from typing import Any, Protocol

from motor.motor_asyncio import AsyncIOMotorClientSession
from src.core.protocols import ReviewOperations
from src.core.uow import MongoUOW
from src.movies.repositories import MongoMovieRepository, MongoUserRepository
from src.movies.repositories.protocols import MovieRepository, UserRepository


class MongoUserMovieUOW(MongoUOW):
    user_repo: UserRepository
    movie_repo: MovieRepository

    def __init__(self, session: AsyncIOMotorClientSession) -> None:
        self._session = session
        self.user_repo = MongoUserRepository(self._session)
        self.movie_repo = MongoMovieRepository(self._session)


class UserMovieService(ReviewOperations, Protocol):
    def __init__(self, uow: MongoUserMovieUOW) -> None: ...
    async def rate_movie(self, user_id: Any, movie_id: Any, value: float) -> None: ...
    async def add_review(self, user_id: Any, movie_id: Any, review: str) -> None: ...
    async def update_review(self, user_id: Any, movie_id: Any, review: str) -> None: ...
    async def delete_review(self, user_id: Any, movie_id: Any) -> None: ...
