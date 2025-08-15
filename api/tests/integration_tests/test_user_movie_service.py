import pytest
from src.movies.repositories.protocols import MovieRepository, UserRepository
from src.movies.services.protocols import UserMovieService


async def test_service_can_add_review(
    data,
    movie_repo: MovieRepository,
    user_repo: UserRepository,
    user_movie_service: UserMovieService,
):
    user_id, movie_id, review = data['user_id'], data['movie_id'], data['review']

    await user_movie_service.add_review(user_id, movie_id, review)

    movie_reviews = await movie_repo.reviews(movie_id)
    user_reviews = await user_repo.reviews(user_id)

    assert movie_reviews == [{'user_id': user_id, 'review': review}], 'Ошибка получения данных'
    assert user_reviews == [{'movie_id': movie_id, 'review': review}], 'Ошибка получения данных'


async def test_service_can_delete_review(
    data,
    movie_repo: MovieRepository,
    user_repo: UserRepository,
    user_movie_service: UserMovieService,
):
    user_id, movie_id, review = data['user_id'], data['movie_id'], data['review']
    await user_movie_service.add_review(user_id, movie_id, review)

    await user_movie_service.delete_review(user_id, movie_id)

    movie_reviews = await movie_repo.reviews(movie_id)
    user_reviews = await user_repo.reviews(user_id)

    assert movie_reviews == user_reviews == [], 'Ошибка получения данных'


async def test_service_can_update_review(
    data,
    movie_repo: MovieRepository,
    user_repo: UserRepository,
    user_movie_service: UserMovieService,
):
    user_id, movie_id, review_old = data['user_id'], data['movie_id'], data['review']
    review_new = 'Movie is bad'
    await user_movie_service.add_review(user_id, movie_id, review_old)

    await user_movie_service.update_review(user_id, movie_id, review_new)

    movie_reviews = await movie_repo.reviews(movie_id)
    user_reviews = await user_repo.reviews(user_id)

    assert movie_reviews == [{'user_id': user_id, 'review': review_new}], 'Ошибка получения данных'
    assert user_reviews == [{'movie_id': movie_id, 'review': review_new}], 'Ошибка получения данных'


async def test_user_cant_add_review_on_same_film_twice(data, user_movie_service: UserMovieService):
    user_id, movie_id, review = data['user_id'], data['movie_id'], data['review']

    await user_movie_service.add_review(user_id, movie_id, review)

    with pytest.raises(Exception, match='This user already has review on movie'):
        await user_movie_service.add_review(user_id, movie_id, review)


async def test_service_cant_update_non_existed_review(data, user_movie_service: UserMovieService):
    user_id, movie_id, review = data['user_id'], data['movie_id'], data['review']

    with pytest.raises(Exception, match='There is no review with this user_id'):
        await user_movie_service.update_review(user_id, movie_id, review)


async def test_get_movie_rating(
    data,
    movie_repo: MovieRepository,
    user_repo: UserRepository,
    user_movie_service: UserMovieService,
):
    user_id, movie_id, value = data['user_id'], data['movie_id'], 7

    await user_movie_service.rate_movie(user_id, movie_id, value)

    rating = await movie_repo.rating(movie_id)
    user_data = await user_repo.get_data(user_id)
    user_assessement = user_data['ratings'][0]['value']

    assert rating == value, 'Неправильный рейтинг фильма'
    assert user_assessement == value, 'Неправильный рейтинг фильма'


async def test_can_rate_few_movies(
    data,
    movie_repo: MovieRepository,
    user_movie_service: UserMovieService,
):
    user_id, movie1_id, value1 = data['user_id'], data['movie_id'], 7
    movie2_id, value2 = 'asddd', 10

    await user_movie_service.rate_movie(user_id, movie1_id, value1)
    await user_movie_service.rate_movie(user_id, movie2_id, value2)

    rating1 = await movie_repo.rating(movie1_id)
    rating2 = await movie_repo.rating(movie2_id)

    assert rating1 == value1, 'Неправильный рейтинг фильма 1'
    assert rating2 == value2, 'Неправильный рейтинг фильма 2'


async def test_can_update_assessment(
    data,
    movie_repo: MovieRepository,
    user_movie_service: UserMovieService,
):
    user_id, movie_id = data['user_id'], data['movie_id']
    old_value, new_value = 7, 3

    await user_movie_service.rate_movie(user_id, movie_id, old_value)
    await user_movie_service.rate_movie(user_id, movie_id, new_value)

    rating = await movie_repo.rating(movie_id)

    assert rating == new_value, 'Неправильный рейтинг фильма'


async def test_returns_right_average_rating(
    data,
    movie_repo: MovieRepository,
    user_movie_service: UserMovieService,
):
    movie_id = data['movie_id']

    import random
    import uuid

    ratings = []

    for _ in range(50):
        user_id = str(uuid.uuid4())
        value = random.randint(1, 10)
        ratings.append(value)
        await user_movie_service.rate_movie(user_id, movie_id, value)

    rating = await movie_repo.rating(movie_id)

    assert rating == round(sum(ratings) / len(ratings), 1), 'Неправильный рейтинг фильма'
