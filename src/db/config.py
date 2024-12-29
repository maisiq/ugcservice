from os import getenv

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


CONN_URI = getenv('MONGODB_URI')


def get_db() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient(CONN_URI)
    return client['movies']

