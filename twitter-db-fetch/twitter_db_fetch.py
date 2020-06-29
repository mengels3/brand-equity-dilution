from pymongo import MongoClient
import pymongo
import requests
import config
import json
import re
import time
import datetime
from database_client import DatabaseClient

fetch_sleep_timeout_in_sec = 3


def fetch_latest_tweets(query, max_id, batch_size):
    # url-encoded payload
    payload = {
        'q': query,
        'result_type': 'recent',
        'count': batch_size,
        'include_entities': 'false',
        'tweet_mode': 'extended',
    }

    if max_id is not None:
        payload['max_id'] = max_id

    # headers
    bearer_token = 'Bearer ' + config.secrets["twitter-bearer-token"]
    headers = {'Authorization': bearer_token}

    # send request to twitter api
    r = requests.get(
        "https://api.twitter.com/1.1/search/tweets.json", params=payload, headers=headers)

    if r.status_code == 200:
        # load json string into python dictionary
        data = json.loads(r.text)

        # retrieve max_id for pagination
        max_id = None
        next_results_str = None
        more_data_availabe = False
        if('next_results' in data['search_metadata']):
            next_results_str = data['search_metadata']['next_results']
            more_data_availabe = True

            regex = r'max_id=(\d*)'
            max_id = int(re.findall(regex, next_results_str)[0])

        # retrieve index of the most recent tweet fetched
        most_recent_tweet_id = data['search_metadata']['max_id']

        print('Successfully fetched ' +
              str(len(data['statuses'])) + ' tweets.')

        # transform tweets
        tweets = list(
            map(lambda tweet: transform_tweet(tweet), data['statuses']))

        return {
            'max_id': max_id,
            'tweets': tweets,
            'most_recent_tweet_id': most_recent_tweet_id,
            'more_data_available': more_data_availabe
        }
    else:
        raise Exception("Fetching twitter content did not work!" + "\n\t" + "Status: " +
                        str(r.status_code) + "\n\t" + "Message: " + r.text)


def transform_tweet(tweet):

    isRetweet = False
    retweetedStatusIdStr = None
    if 'retweeted_status' in tweet and tweet['retweeted_status'] is not None:
        isRetweet = True
        retweetedStatusIdStr = tweet['retweeted_status']['id_str']

    return {
        'created_at': tweet['created_at'],
        'id_str': tweet['id_str'],
        'id_int': tweet['id']
        'full_text': tweet['full_text'],
        'isRetweet': isRetweet,
        'retweeted_status_id_str': retweetedStatusIdStr,
        'lang': tweet['lang'],
        'user': {
            'id_str': tweet['user']['id_str'],
            'id_int': tweet['user']['id'],
            'name': tweet['user']['name'],
            'screen_name': tweet['user']['screen_name'],
            'location': tweet['user']['location'],
            'followers_count': tweet['user']['followers_count'],
            'friends_count': tweet['user']['friends_count'],
            'listed_count': tweet['user']['listed_count'],
            'favourites_count': tweet['user']['favourites_count'],
            'profile_image_url': tweet['user']['profile_image_url'],
        }
    }

# TODO consider fetch_batch_size


def populateTweetsInDatabase(collection, query, fetch_iterations, fetch_batch_size, dbClient):

    print("\n------ Populating database collection '" + collection + "' for query '" +
          query + "' with at most " + str(fetch_iterations*fetch_batch_size) + " tweets. ------")

    latest_saved_index = dbClient.getLatestTweetId(
        collection, 5, 10)
    print('Wait for 10 seconds until storing documents to collection.')
    time.sleep(10)

    max_id = None

    # if there has been a lot of tweets or we are doing an inital fetch we will at most do 50 requests a 20 tweets => saving 1000 tweets at max
    for i in range(fetch_iterations):
            # rate limiting
        if i > 0:
            print("Sleep for " + str(fetch_sleep_timeout_in_sec) + " seconds.")
            time.sleep(fetch_sleep_timeout_in_sec)
        # fetch tweets
        result = fetch_latest_tweets(query, max_id, fetch_batch_size)

        if result['most_recent_tweet_id'] == latest_saved_index:
            print("-> There are no new tweets. Collection is already up to date.")
            break

        # if there is no more data do be fetched (because we collected all tweets of the last 7 days) exit the loop
        if result["more_data_available"] == False:

            print(
                "-> All tweets for the last 7 days have been successfully fetched and stored.")
            break
            # if the max_id index (which determines that we want to fetch tweets older than or equal than this id) is smaller than
            # the index of the oldest tweet saved, than we are fetching data we already have stored in our database!
        if result["max_id"] < latest_saved_index:
            # 1. remove all tweets <= the latest saved index
            fetched_tweets = result["tweets"]
            fetched_tweets_more_recent_than_last_saved = list(filter(
                lambda tweet: int(tweet["id_str"]) > latest_saved_index, fetched_tweets))
            # 2. save remaining in database
            saveTweets(
                collection, fetched_tweets_more_recent_than_last_saved, 5, 10, dbClient)

            print("-> All new tweets have been successfully fetched and stored.")
            # 3. exit for loop
            break
        else:
            # just save items and set max_id for pagination
            max_id = result["max_id"]
            saveTweets(collection, result["tweets"], 5, 10, dbClient)


def saveTweets(collection, tweets, retries, timeoutSec, dbClient):
    for i in range(retries):
        try:
            dbClient.saveDocuments(
                collection, tweets)
            break
        except Exception as e:
            if i == retries-1:
                raise e
            print(
                'There was an error with writing tweets to database (try ' + str(i+1) + '/' + str(retries) + '): ' + str(e))
            print('Sleep for ' + str(timeoutSec) + ' seconds and try again.')
            time.sleep(timeoutSec)


def main():
    start = time.time()
    print("Starttime: %s" % str(datetime.datetime.now()))
    dbClient = DatabaseClient()
    # for some reason we have to do this once (maybe to establish connection but dunno)
    dbClient.getLatestTweetId('audi_etron', 1, 1)
    # maybe wait for connection?
    time.sleep(1)
    # 40 tweets every 3 seconds = 12.000 tweets per 15 minutes
    populateTweetsInDatabase(
        'audi_etron', 'audi etron OR audi e-tron', 30, 30, dbClient)
    populateTweetsInDatabase('audi', 'audi', 30, 30, dbClient)
    populateTweetsInDatabase(
        'google_stadia', 'google stadia OR stadia', 30, 30, dbClient)
    populateTweetsInDatabase('google', 'google', 30, 30, dbClient)
    populateTweetsInDatabase(
        'volkswagen', 'vw OR volkswagen', 30, 30, dbClient)
    populateTweetsInDatabase(
        'volkswagen_id3', 'vw id.3 OR volkswagen id.3 OR vw id3 OR volkswagen id3', 30, 30, dbClient)
    populateTweetsInDatabase(
        'mercedes', 'mercedes OR mercedes-benz', 30, 30, dbClient)
    populateTweetsInDatabase(
        'mercedes_eqc', 'mercedes eqc OR mercedes-benz eqc OR benz eqc', 30, 30, dbClient)

    print('Script took ' + str(time.time() - start) + ' seconds to execute.')
    print("Endtime: %s" % str(datetime.datetime.now()))


if __name__ == "__main__":
    main()
