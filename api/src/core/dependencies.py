from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from src.db.mongo_client import get_db_client
from src.logger.logger import get_logger


async def get_session(client: AsyncIOMotorClient = Depends(get_db_client, use_cache=True)):
    get_logger().debug('get_session(): Trying to start db session...')
    session = await client.start_session()
    yield session
    await session.end_session()
