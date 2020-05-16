from pymongo import MongoClient
import pymongo
import requests
import config
import json
import re
import time
from database_client import DatabaseClient

dbClient = DatabaseClient()

query = 'audi etron OR audi e-tron'


def fetch_latest_tweets(query, max_id):
    # url-encoded payload
    payload = {
        'q': query,
        'result_type': 'recent',
        'count': 50,
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
        'full_text': tweet['full_text'],
        'isRetweet': isRetweet,
        'retweeted_status_id_str': retweetedStatusIdStr,
        'lang': tweet['lang'],
        'user': {
            'id_str': tweet['user']['id_str'],
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


def save_data_to_db(tweets):
    db_connection_string = config.secrets["db-connection-string"]
    client = MongoClient(db_connection_string)
    tweet_collection = client["coins-brand-equity-dilution-database"].tweets

    tweet_collection.insert_many(tweets)
    print('Successfully saved ' + str(len(tweets)) + ' tweets to database.')


def main(latest_saved_index, max_id):
        # if there has been a lot of tweets or we are doing an inital fetch we will at most do 50 requests a 20 tweets => saving 1000 tweets at max
    for i in range(50):
        # rate limiting
        if i > 0:
            print("Sleep for 1 seconds.")
            time.sleep(1)
        # fetch tweets
        result = fetch_latest_tweets(query, max_id)

        if result['most_recent_tweet_id'] == latest_saved_index:
            print("There are no new tweets. Database is already up to date.")
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
            save_data_to_db(fetched_tweets_more_recent_than_last_saved)
            print("-> All new tweets have been successfully fetched and stored.")
            # 3. exit for loop
            break
        else:
            # just save items and set max_id for pagination
            max_id = result["max_id"]
            save_data_to_db(result["tweets"])


# MAIN

if __name__ == "__main__":

    main(dbClient.getLatestTweetId(), None)
