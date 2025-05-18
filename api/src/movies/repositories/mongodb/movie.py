from motor.motor_asyncio import AsyncIOMotorClientSession

from src.db.config import MONGO_DB, MongoCollections
from src.core.exceptions import EntityDoesNotExist, EntityAlreadyExists


class MongoMovieRepository:
    def __init__(self, session: AsyncIOMotorClientSession):
        self._session = session
        self._coll = self._session.client[MONGO_DB][MongoCollections.movies]

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
            {'_id': 0, 'rating': {'$avg': '$ratings.value'}},
            session=self._session,
        )
        if data is not None:
            resp = {'rating': round(data['rating'], 1)}
        else:
            raise EntityDoesNotExist('Movie doesnt exist')
        return resp

    async def add_review(self, user_id, movie_id, review):
        result = await self._coll.find_one(
            {'_id': movie_id, 'reviews.user_id': user_id},
            session=self._session,
        )

        if result:
            raise EntityAlreadyExists('This user already has review on movie')

        result = await self._coll.update_one(
            {'_id': movie_id},
            {'$push': {
                'reviews': {'user_id': user_id, 'review': review}
            }},
            session=self._session,
            upsert=True,
        )
        return result.acknowledged

    async def update_review(self, user_id, movie_id, review):
        result = await self._coll.update_one(
            {'_id': movie_id, 'reviews.user_id': user_id},
            {'$set': {'reviews.$.review': review}},
            session=self._session,
        )
        if result.matched_count == 0:
            raise EntityDoesNotExist('There is no review with this id')
        return result.acknowledged

    async def delete_review(self, user_id, movie_id):
        result = await self._coll.update_one(
            {'_id': movie_id, 'reviews.user_id': user_id},
            {'$pull': {'reviews': {'user_id': user_id}}},
            session=self._session,
        )
        return result.acknowledged

    async def rate(self, user_id, movie_id, value):
        result = await self._coll.update_one(
            {'_id': movie_id, 'ratings.user_id': user_id},
            {'$set': {'ratings.$.value': value}},
        )

        if result.matched_count == 0:
            result = await self._coll.update_one(
                {'_id': movie_id},
                {'$push': {'ratings': {'user_id': user_id, 'value': value}}},
                session=self._session,
                upsert=True,
            )
        return result.acknowledged
