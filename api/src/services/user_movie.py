from src.db.repositories.protocols import MovieRepository, UserRepository
from src.core.protocols import UOW


class MongoUserMovieService:
    def __init__(self, uow: UOW, user_repo: UserRepository, movie_repo: MovieRepository):
        self._uow = uow
        self._user_repo = user_repo
        self._movie_repo = movie_repo

    async def add_review(self, user_id, movie_id, review):
        async with self._uow as uow:
            await self._user_repo.add_review(user_id, movie_id, review)
            await self._movie_repo.add_review(user_id, movie_id, review)
            await uow.commit()

    async def update_review(self, user_id, movie_id, review):
        async with self._uow as uow:
            await self._user_repo.update_review(user_id, movie_id, review)
            await self._movie_repo.update_review(user_id, movie_id, review)
            await uow.commit()

    async def delete_review(self, user_id, movie_id):
        async with self._uow as uow:
            await self._user_repo.delete_review(user_id, movie_id)
            await self._movie_repo.delete_review(user_id, movie_id)
            await uow.commit()

    async def like(self, user_id, review_id):
        raise NotImplementedError
