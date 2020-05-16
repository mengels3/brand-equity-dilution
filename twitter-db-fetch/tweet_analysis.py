from pymongo import MongoClient
import pymongo
import config
from database_client import DatabaseClient

dbClient = DatabaseClient()

tweets = list(dbClient.tweet_collection.find())
print("Currently there are " + str(len(tweets)) +
      " tweets stored in the database.")

max_id = max(list(map(lambda tweet: int(tweet['id_str']), tweets)))
print("Id of latest fetched tweet is " + str(max_id) + ".")
