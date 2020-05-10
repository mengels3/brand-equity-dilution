from pymongo import MongoClient
import requests
import config
import json
import re


query = 'audi etron OR audi e-tron'


def fetch_latest_tweets(query, max_id):
    # url-encoded payload
    payload = {
        'q': query,
        'result_type': 'recent',
        'count': 3,
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
        next_results_str = data['search_metadata']['next_results']
        regex = r'max_id=(\d*)'
        max_id = int(re.findall(regex, next_results_str)[0])
        # retrieve index of the most recent tweet fetched
        most_recent_tweet_id = data['search_metadata']['max_id']

        print('Successfully fetched ' +
              str(len(data['statuses'])) + ' tweets.')

        return {
            'max_id': max_id,
            'tweets': data['statuses'],
            'most_recent_tweet_id': most_recent_tweet_id
        }
    else:
        raise Exception("Fetching twitter content did not work!" + "\n\t" + "Status: " +
                        str(r.status_code) + "\n\t" + "Message: " + r.text)


def save_data_to_db(tweets):
    db_connection_string = config.secrets["db-connection-string"]
    client = MongoClient(db_connection_string)

    tweet_collection = client["coins-brand-equity-dilution-database"].tweets

    tweet_collection.insert_many(tweets)
    print('Successfully saved ' + str(len(tweets)) + ' tweets to database.')


# return -1 if there have not been stored tweets yet, otherwise the (integer) id of the latest saved tweet
def get_latest_saved_index():
    print('Retrieving index of most recent tweet stored in database.')
    f = open('last_saved_tweet_index.txt', 'r')
    index = f.readline()
    if index is "":
        return -1
    else:
        return int(index)


def set_latest_saved_index(index):
    print('Updating index of most recent tweet stored in database.')
    f = open('last_saved_tweet_index.txt', 'w')
    f.write(str(index))
    f.close()


# MAIN

# init variables
latest_saved_index = get_latest_saved_index()
max_id = None

# if there has been a lot of tweets or we are doing an inital fetch we will at most do 50 requests a 100 tweets => saving 5000 tweets at max
for i in range(2):

    result = fetch_latest_tweets(query, max_id)

    if result['most_recent_tweet_id'] == latest_saved_index:
        print("There are no new tweets. Database is already up to date.")
        break

    # extract the id of the most recent tweet  of the first fetch to update lastest_saved_index
    if i == 0:
        set_latest_saved_index(result["most_recent_tweet_id"])

    # if the max_id index (which determines that we want to fetch tweets older than or equal than this id) is smaller than
    # the index of the oldest tweet saved, than we are fetching data we already have stored in our database!
    if result["max_id"] < latest_saved_index:
        # 1. remove all tweets <= the latest saved index
        fetched_tweets = result["tweets"]
        fetched_tweets_more_recent_than_last_saved = filter(
            lambda tweet: tweet["id"] <= latest_saved_index, fetched_tweets)
        # 2. save remaining in database
        save_data_to_db(fetched_tweets_more_recent_than_last_saved)
        # 3. exit for loop
        break
    else:
        # just save items and set max_id for pagination
        max_id = result["max_id"]
        save_data_to_db(result["tweets"])

    i += 1
