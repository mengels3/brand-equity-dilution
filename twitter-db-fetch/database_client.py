from pymongo import MongoClient
import pymongo
import config


class DatabaseClient:
    def __init__(self):
        db_connection_string = config.secrets["db-connection-string"]
        self.client = MongoClient(db_connection_string)
        self.tweet_collection = self.client["coins-brand-equity-dilution-database"].tweets

    def getLatestTweetId(self):
        tweets = list(self.tweet_collection.find())

        if len(tweets) == 0:
            return -1

        max_id = max(list(map(lambda tweet: int(tweet['id_str']), tweets)))
        print("Most recent tweet in database has id " + str(max_id) + ".")
        return max_id
