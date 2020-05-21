from pymongo import MongoClient
import pymongo
import config
import time


class DatabaseClient:
    def __init__(self):
        db_connection_string = config.secrets["db-connection-string"]
        self.client = MongoClient(db_connection_string)
        self.database = self.client["coins-brand-equity-dilution-database"]
        print('Initalized database client.')

    def getLatestTweetId(self, collection_name, retries, timeoutSec):
        tweets = None
        for i in range(retries):
            try:
                collection = self.database[collection_name]
                tweets = list(collection.find({}))
                break
            except Exception as e:
                if i == retries-1:
                    raise e
                print(
                    'There was an error with reading from database (try ' + str(i+1) + '/' + str(retries) + '): ' + str(e))
                print('Sleep for ' + str(timeoutSec) +
                      ' seconds and try again.')
                time.sleep(timeoutSec)

        if len(tweets) == 0:
            print("No tweets stored in collection " + collection_name)
            return -1

        max_id = max(list(map(lambda tweet: int(tweet['id_str']), tweets)))
        print("Most recent tweet in " + collection_name +
              " collection has id " + str(max_id) + ".")
        return max_id

    def getAllDocuments(self, collection_name):
        return list(self.database[collection_name].find())

    def saveDocuments(self, collection_name, documents):
        collection = self.database[collection_name]
        collection.insert_many(documents)
        print('Successfully saved ' + str(len(documents)) +
              ' documents to database ' + collection_name + '.')
