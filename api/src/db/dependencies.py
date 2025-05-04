from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession

from src.db.config import get_db_client
from .repositories.mongodb.movie import MongoMovieRepository
from .repositories.mongodb.user import MongoUserRepository


async def get_session(client: AsyncIOMotorClient = Depends(get_db_client, use_cache=False)):
    session = await client.start_session()
    yield session
    await session.end_session()


async def user_repo(session: AsyncIOMotorClientSession = Depends(get_session, use_cache=False)):
    yield MongoUserRepository(session)


async def movie_repo(session: AsyncIOMotorClientSession = Depends(get_session, use_cache=False)):
    yield MongoMovieRepository(session)
