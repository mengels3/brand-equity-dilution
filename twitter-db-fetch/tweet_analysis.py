from pymongo import MongoClient
import pymongo
import config
from database_client import DatabaseClient

dbClient = DatabaseClient()

# dbClient.getLatestTweetId('audi', 3, 5)
res = dbClient.getAllDocumentsInChunks('audi', 50, 1)
print(len(res))

# dbClient.getAllDocuments('audi')

# collection = 'audi'

# tweets = dbClient.getAllDocuments(collection)
# print("Currently there are " + str(len(tweets)) +
#       " tweets stored in the collection '" + collection + "'.")

# latestId = dbClient.getLatestTweetId(collection, 3, 5)

# max_id = max(list(map(lambda tweet: int(tweet['id_str']), tweets)))
# print("Id of latest fetched tweet is " + str(max_id) + ".")
