import pytest
from src.config.db import MONGO_DB, MongoCollections


@pytest.mark.mongo
async def test_can_add_bookmark(data, db_client, mongo_user_repo):

    await mongo_user_repo.add_bookmark(data['user_id'], data['movie_id'])

    users_col = db_client[MONGO_DB][MongoCollections.users]
    result = await users_col.find_one(
        {'_id': data['user_id']},
        {'bookmarks': 1},
    )

    assert result.get('bookmarks') == [data['movie_id']], 'Ошибка получаения данных'


@pytest.mark.mongo
async def test_cant_add_same_movie_to_bookmarks(data, db_client, mongo_user_repo):
    """You can add same bookmark to the user data, but it won't dublicate
    and won't throw an error.
    """

    await mongo_user_repo.add_bookmark(data['user_id'], data['movie_id'])
    await mongo_user_repo.add_bookmark(data['user_id'], data['movie_id'])

    users_col = db_client[MONGO_DB][MongoCollections.users]
    result = await users_col.find_one(
        {'_id': data['user_id']},
        {'bookmarks': 1},
    )

    assert len(result.get('bookmarks')) == 1, 'Длина списка не совпадает'


@pytest.mark.mongo
async def test_can_remove_bookmark(data, db_client, mongo_user_repo):
    await mongo_user_repo.add_bookmark(data['user_id'], data['movie_id'])

    await mongo_user_repo.remove_bookmark(data['user_id'], data['movie_id'])

    db = db_client[MONGO_DB]
    users = db[MongoCollections.users]
    result = await users.find_one(
        {'_id': data['user_id']},
        {'bookmarks': 1},
    )

    assert result.get('bookmarks') == list(), 'Ошибка удаления данных'


@pytest.mark.mongo
async def test_can_remove_non_existed_bookmark(data, mongo_user_repo):
    user_id = data['user_id']

    await mongo_user_repo.remove_bookmark(user_id, data['movie_id'])

    bookmarks = await mongo_user_repo.bookmarks(user_id)

    assert bookmarks == list(), 'Ошибка удаления данных'


@pytest.mark.mongo
async def test_get_user_data(data, mongo_user_repo):
    user_id, movie_id, review = data['user_id'], data['movie_id'], data['review']

    await mongo_user_repo.add_bookmark(user_id, movie_id)
    await mongo_user_repo.add_review(user_id, movie_id, review)

    expected_data = {
        'user_id': user_id,
        'reviews': [
            {'movie_id': movie_id, 'review': review}
        ],
        'bookmarks': [movie_id]
    }

    data = await mongo_user_repo.get_data(user_id)

    assert expected_data == data, 'Данные не совпадают'


@pytest.mark.mongo
async def test_get_user_bookmarks(data, mongo_user_repo):
    user_id, movie_id = data['user_id'], data['movie_id']

    await mongo_user_repo.add_bookmark(user_id, movie_id)

    bookmarks = await mongo_user_repo.bookmarks(user_id)

    expected_data = [movie_id]
    assert expected_data == bookmarks, 'Данные не совпадают'


@pytest.mark.mongo
async def test_get_user_reviews(data, mongo_user_repo):
    user_id, movie_id, review = data['user_id'], data['movie_id'], data['review']

    await mongo_user_repo.add_review(user_id, movie_id, review)

    data = await mongo_user_repo.reviews(user_id)

    expected_data = [{'movie_id': movie_id, 'review': review}]
    assert expected_data == data, 'Данные не совпадают'
