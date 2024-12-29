from motor.motor_asyncio import AsyncIOMotorDatabase

from src.db.config import get_db

class UserDoesNotExist(Exception):
    pass


class MongoRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_user_bookmarks(self, user_id: int):
        result = await self.db['users'].find_one({"_id": user_id}, {'_id': 0, 'bookmarks': 1})
        print(result)
        return result.get('bookmarks') or []

    async def add_movie_to_user_bookmarks(self, user_id: int, movie_id: str) -> bool:
        result = await self.db['users'].update_one({"_id": user_id}, {"$addToSet": {"bookmarks": movie_id}})
        if result.matched_count == 0:
            raise UserDoesNotExist
        if result.modified_count == 0:
            return False
        return True

    async def remove_movie_from_user_bookmarks(self, user_id: int, movie_id):
        result = await self.db['users'].update_one({"_id": user_id}, {"$pull": {"bookmarks": movie_id}})
        if result.matched_count == 0:
            raise UserDoesNotExist
        if result.modified_count == 0:
            return False
        return True


mongo_repo = lambda: MongoRepository(get_db())