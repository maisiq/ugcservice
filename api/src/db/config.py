import logging
from enum import Enum
from os import getenv
from typing import AsyncGenerator

import backoff
from fastapi import status
from fastapi.exceptions import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError

CONN_URI = getenv('MONGODB_URI')

MONGO_DB = 'movies'


class MongoCollections(str, Enum):
    users = 'users'
    movies = 'movies'


def database_exception_handler(e):
    logging.error(e)
    raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail='Service temporary unavailable')


@backoff.on_exception(
    backoff.expo,
    ServerSelectionTimeoutError,
    max_tries=5,
    on_giveup=database_exception_handler
)
async def get_db_client() -> AsyncGenerator[AsyncIOMotorClient, None]:
    client = AsyncIOMotorClient(
        CONN_URI, 
        maxpoolsize=100,
        serverselectiontimeoutms=5000,
    )
    logging.info('Пытаюсь подключиться к MongoDB')
    db = client['movies']
    await db.command({'ping': 1})
    logging.info('Подключение к MongoDB установлено')
    return client

