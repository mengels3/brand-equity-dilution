from pymongo import MongoClient
import requests
import config

uri = config.secrets["db-connection-string"]
client = MongoClient(uri)

items = client["coins-brand-equity-dilution-database"].items

items = items.find_one()
print(items)
