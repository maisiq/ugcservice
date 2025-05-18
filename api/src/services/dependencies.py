from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession

from src.core.uow import MongoUOW
from src.db.dependencies import get_session
from src.movies.repositories.mongodb.movie import MongoMovieRepository
from src.movies.repositories.mongodb.user import MongoUserRepository
from src.services.user_movie import MongoUserMovieService


async def user_movie_service(session: AsyncIOMotorClientSession = Depends(get_session, use_cache=False)):
    uow = MongoUOW(session)
    user_repo = MongoUserRepository(session)
    movie_repo = MongoMovieRepository(session)

    yield MongoUserMovieService(uow, user_repo, movie_repo)
