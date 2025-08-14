from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession
from src.analytics.repository.mongo_view import MongoViewRepository
from src.core.dependencies import get_session


async def view_repo(session: AsyncIOMotorClientSession = Depends(get_session)):
    yield MongoViewRepository(session)
