from enum import Enum
from os import getenv

CONN_URI = getenv('MONGODB_URI')
MONGO_DB = getenv('MONGODB_NAME', 'movies')


class MongoCollections(str, Enum):
    users = 'users'
    movies = 'movies'
