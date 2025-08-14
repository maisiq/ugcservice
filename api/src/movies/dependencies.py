from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession
from src.core.dependencies import get_session
from src.core.uow import MongoUOW

from .repositories import MongoMovieRepository, MongoUserRepository
from .services.user_movie import MongoUserMovieService


async def user_movie_service(session: AsyncIOMotorClientSession = Depends(get_session, use_cache=False)):
    uow = MongoUOW(session)
    user_repo = MongoUserRepository(session)
    movie_repo = MongoMovieRepository(session)

    yield MongoUserMovieService(uow, user_repo, movie_repo)


async def user_repo(session: AsyncIOMotorClientSession = Depends(get_session, use_cache=False)):
    yield MongoUserRepository(session)


async def movie_repo(session: AsyncIOMotorClientSession = Depends(get_session, use_cache=False)):
    yield MongoMovieRepository(session)
