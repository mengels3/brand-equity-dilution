from pymongo import MongoClient
import pymongo
import config

db_connection_string = config.secrets["db-connection-string"]
client = MongoClient(db_connection_string)
tweet_collection = client["coins-brand-equity-dilution-database"].tweets

tweets = list(tweet_collection.find())
print("Currently there are " + str(len(tweets)) +
      " tweets stored in the database.")
