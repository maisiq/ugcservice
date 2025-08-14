from typing import AsyncGenerator

import backoff
from async_lru import alru_cache
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from src.config.db import CONN_URI
from src.core.utils import service_down_handler
from src.logger.logger import get_logger


@backoff.on_exception(
    backoff.expo,
    ConnectionFailure,
    max_tries=5,
    on_giveup=service_down_handler,
)
@alru_cache
async def get_db_client() -> AsyncGenerator[AsyncIOMotorClient, None]:
    logger = get_logger()

    client = AsyncIOMotorClient(
        CONN_URI,
        maxpoolsize=50,
        serverselectiontimeoutms=5000,
    )
    logger.info('get_db_client(): Trying to connect to DB server')
    try:
        await client.admin.command('ping')
    except ConnectionFailure as e:
        logger.error("get_db_client(): Couldn't connect to DB. Details: %s", e)
        raise ConnectionFailure('Can not ping the DB server')

    logger.info('get_db_client(): Database connection is established')
    return client
    return client
