from pymongo import MongoClient
import pymongo
import config

db_connection_string = config.secrets["db-connection-string"]
client = MongoClient(db_connection_string)
tweet_collection = client["coins-brand-equity-dilution-database"].tweets

tweets = tweet_collection.find()
print(tweets)

for tweet in tweets:
    print(tweet['id_str'])
