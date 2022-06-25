import collections
from http import client
from pymongo import MongoClient

client = MongoClient('localhost',27017)

db = client.quiz_database

user = db.user
quizes = db.Quizes

# print(list(creaters.find()))
