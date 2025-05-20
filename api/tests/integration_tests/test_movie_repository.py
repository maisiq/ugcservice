import pytest

from motor.motor_asyncio import AsyncIOMotorClient

from src.db.config import MONGO_DB, MongoCollections


@pytest.mark.mongo
async def test_repo_returns_reviews(data, db_client: AsyncIOMotorClient, mongo_movie_repo):
    user_id, movie_id, review = data['user_id'], data['movie_id'], data['review']

    expected_data = [{'user_id': user_id, 'review': review}]

    coll = db_client[MONGO_DB][MongoCollections.movies]
    await coll.insert_one(
        {'_id': movie_id, 'reviews': expected_data}
    )

    data = await mongo_movie_repo.reviews(movie_id)

    assert expected_data == data, 'Ошибка получения данных'


@pytest.mark.mongo
async def test_repo_returns_rating(data, db_client: AsyncIOMotorClient, mongo_movie_repo):
    user_id, movie_id, value = data['user_id'], data['movie_id'], 10

    coll = db_client[MONGO_DB][MongoCollections.movies]
    await coll.insert_one(
        {'_id': movie_id, 'ratings': [{'user_id': user_id, 'value': value}]}
    )

    movie_rating = await mongo_movie_repo.rating(movie_id)

    assert movie_rating['rating'] == round(value, 1), 'Ошибка получения данных'
