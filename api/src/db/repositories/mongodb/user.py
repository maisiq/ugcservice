from motor.motor_asyncio import AsyncIOMotorClientSession

from src.db.config import MONGO_DB, MongoCollections


class MongoUserRepository:
    def __init__(self, session: AsyncIOMotorClientSession):
        self._session = session
        self._coll = self._session.client[MONGO_DB][MongoCollections.users] # ADD CONSTANT VALUE TO CONFIG

    async def add_bookmark(self, user_id, movie_id): 
        result = await self._coll.update_one(
            {"_id": user_id}, 
            {"$addToSet": {"bookmarks": movie_id}}, 
            upsert=True,
            session=self._session,
        )
        return result.acknowledged

    async def remove_bookmark(self, user_id, movie_id):
        result = await self._coll.update_one(
            {"_id": user_id}, 
            {"$pull": {"bookmarks": movie_id}},
            session=self._session,
        )
        return result.acknowledged

    async def bookmarks(self, user_id):
        result = await self._coll.find_one(
            {"_id": user_id}, 
            {'_id': 0, 'bookmarks': 1},
            session=self._session,
        )
        return result.get('bookmarks') if result is not None else []

    async def get_data(self, user_id): 
        return await self._coll.find_one(
            {"_id": user_id},
            {"_id": 0, "reviews": 1, "bookmarks": 1, "user_id": "$_id"},
            session=self._session,
        )

    async def reviews(self, user_id): 
        result = await self._coll.find_one(
            {"_id": user_id},
            {'_id': 0, 'reviews': 1},
            session=self._session,
        )
        return result.get('reviews') if result is not None else []
    
    async def add_review(self, user_id, movie_id, review):
        result = await self._coll.find_one(
            {'_id': movie_id, 'reviews.user_id': user_id},
            session=self._session,
        )

        if result:
            raise Exception('This user already has review on movie')

        result = await self._coll.update_one(
            {'_id': user_id},
            {"$push": {
                "reviews": {'movie_id': movie_id, 'review': review}
            }},
            session=self._session,
            upsert=True,
        )
        return result.acknowledged
    
    async def update_review(self, user_id, movie_id, review):
        result = await self._coll.update_one(
            {'_id': user_id, 'reviews.movie_id': movie_id},
            {"$set": {"reviews.$.review": review}},
            session=self._session,
        )
        if result.matched_count == 0:
            raise Exception('There is no review with this id')
        return result.acknowledged

    async def delete_review(self, user_id, movie_id):
        result = await self._coll.update_one(
            {'_id': user_id, 'reviews.movie_id': movie_id},
            {"$pull": {"reviews": {"movie_id": movie_id}}},
            session=self._session,
        )
        return result.acknowledged
