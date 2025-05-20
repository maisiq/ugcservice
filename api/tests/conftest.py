import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient

from src.movies.repositories.mongodb import movie, user
from src.services.user_movie import MongoUserMovieService
from src.core.uow import MongoUOW


def get_mongodb_client():
    TEST_DB_URI = os.getenv('TEST_DB_URI')

    if not TEST_DB_URI:
        raise Exception('TEST_DB_URI env is not set.')

    mongo_client = AsyncIOMotorClient(
        TEST_DB_URI,
        maxpoolsize=100,
        serverselectiontimeoutms=5000,
    )

    return mongo_client


@pytest_asyncio.fixture
async def db_client() -> AsyncGenerator[AsyncIOMotorClient]:
    """Client fixture for MongoDB."""

    mongo_client = get_mongodb_client()
    yield mongo_client

    # Clear database
    for db_name in await mongo_client.list_database_names():
        if db_name in ['config', 'admin', 'local']:
            continue
        database = mongo_client[db_name]

        for collection_name in await database.list_collection_names():
            collection = database[collection_name]
            await collection.drop()
    mongo_client.close()


@pytest_asyncio.fixture(name='mongo_session')
async def get_session(db_client):
    session = await db_client.start_session()
    yield session
    await session.end_session()


@pytest_asyncio.fixture(name='user_repo')
async def get_user_repo(mongo_user_repo) -> AsyncGenerator[MongoUserMovieService]:
    '''Fixture separated from concrete Mongo implementation.
       It can be any repo (Mongo, In-memory etc.). But for now it using MongoRepo.
    '''
    yield mongo_user_repo


@pytest_asyncio.fixture(name='movie_repo')
async def get_movie_repo(mongo_movie_repo) -> AsyncGenerator[MongoUserMovieService]:
    '''Fixture separated from concrete Mongo implementation.
       It can be any repo (Mongo, In-memory etc.). But for now it using MongoRepo.
    '''
    yield mongo_movie_repo


@pytest_asyncio.fixture(name='mongo_user_repo')
async def get_mongo_user_repo(mongo_session) -> AsyncGenerator[MongoUserMovieService]:
    yield user.MongoUserRepository(mongo_session)


@pytest_asyncio.fixture(name='mongo_movie_repo')
async def get_mongo_movie_repo(mongo_session) -> AsyncGenerator[MongoUserMovieService]:
    yield movie.MongoMovieRepository(mongo_session)


@pytest_asyncio.fixture(name='user_movie_service')
async def get_user_movie_service(mongo_session) -> AsyncGenerator[MongoUserMovieService]:
    uow = MongoUOW(mongo_session)
    user_repo = user.MongoUserRepository(mongo_session)
    movie_repo = movie.MongoMovieRepository(mongo_session)
    yield MongoUserMovieService(uow, user_repo, movie_repo)


@pytest.fixture(name='data', scope='module')
def create_data():
    f = Faker('ru_RU')

    return {
        'user_id': f.uuid4(),
        'movie_id': f.uuid4(),
        'review': f.sentence(4, True),
    }
