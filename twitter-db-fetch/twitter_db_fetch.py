from pymongo import MongoClient
import requests
import config
import json
import re


query = 'audi etron OR audi e-tron'


def fetch_latest_tweets(query):

    # url-encoded payload
    payload = {
        'q': query,
        'result_type': 'recent',
        'count': 3,
        'include_entities': 'false',
        'tweet_mode': 'extended'
    }

    # headers
    bearer_token = 'Bearer ' + config.secrets["twitter-bearer-token"]
    headers = {'Authorization': bearer_token}

    # send request to twitter api
    r = requests.get(
        "https://api.twitter.com/1.1/search/tweets.json", params=payload, headers=headers)

    if r.status_code == 200:
        data = json.loads(r.text)

        next_results_str = data['search_metadata']['next_results']
        regex = r'max_id=(\d*)'
        max_id = int(re.findall(regex, next_results_str)[0])

        return {
            'max_id': max_id,
            'tweets': data['statuses']
        }
    else:
        raise Exception("Fetching twitter content did not work!" + "\n\t" + "Status: " +
                        str(r.status_code) + "\n\t" + "Message: " + r.text)


def save_data_to_db(tweets):
    db_connection_string = config.secrets["db-connection-string"]
    client = MongoClient(db_connection_string)

    tweet_collection = client["coins-brand-equity-dilution-database"].tweets

    tweet_collection.insert_many(tweets)


# MAIN
result = fetch_latest_tweets(query)
tweets = result['tweets']
save_data_to_db(tweets)
