from motor.motor_asyncio import AsyncIOMotorClientSession
from src.config.db import MONGO_DB, MongoCollections

from ..models import View, ViewMessage


class MongoViewRepository:
    def __init__(self, session: AsyncIOMotorClientSession):
        self._session = session
        self._coll = self._session.client[MONGO_DB][MongoCollections.users]

    async def add_view(self, message: ViewMessage):
        """Add user's view progress for the movie. If there is no progress yet, upserts it.
        """
        result = await self._coll.update_one(
            {'_id': str(message.user_id)},
            {'$addToSet': {'views': {'movie_id': message.movie_id, 'timestamp_ms': message.timestamp_ms}}},
            upsert=True,
            session=self._session,
        )
        return result.acknowledged

    async def get_view(self, user_id: str, movie_id: str) -> ViewMessage:
        resp = await self._coll.find_one(
            {'_id': user_id, 'views.movie_id': movie_id},
            {'_id': 0, 'views': {'$elemMatch': {'movie_id': movie_id}}, 'user_id': '$_id'},
            session=self._session,
        )
        if resp is None:
            return ViewMessage(movie_id=movie_id, timestamp_ms=0, user_id=user_id)

        return ViewMessage(
            user_id=resp['user_id'],
            movie_id=resp['views'][0]['movie_id'],
            timestamp_ms=resp['views'][0]['timestamp_ms']
        )

    async def view_list(self, user_id: str) -> list[View]:
        resp = await self._coll.find_one(
            {'_id': user_id},
            {'_id': 0, 'views': 1},
            session=self._session,
        )
        if resp is None:
            return []

        return [View.model_validate(v) for v in resp['views']]
