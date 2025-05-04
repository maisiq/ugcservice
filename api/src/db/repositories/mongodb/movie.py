from motor.motor_asyncio import AsyncIOMotorClientSession

from src.db.config import MONGO_DB, MongoCollections


class MongoMovieRepository:
    def __init__(self, session: AsyncIOMotorClientSession):
        self._session = session
        self._coll = self._session.client[MONGO_DB][MongoCollections.movies] # ADD CONSTANT VALUE TO CONFIG

    async def reviews(self, movie_id): 
        data = await self._coll.find_one(
            {'_id': movie_id}, 
            {'_id': 0, 'reviews': 1},
            session=self._session,
        )
        return data.get('reviews') if data is not None else []

    async def rating(self, movie_id) -> dict[str, str | None]: 
        data = await self._coll.find_one(
            {'_id': movie_id},
            {'_id': 0, 'rating': {'$sum': '$ratings.value'}},
            session=self._session,
        )
        return data if data is not None else {'rating': None}