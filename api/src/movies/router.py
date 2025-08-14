from typing import Annotated, TypeAlias

from fastapi import Body, Depends, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from src.core.exceptions import EntityAlreadyExists, EntityDoesNotExist
from src.core.responses import DEFAULT_RESPONSES
from src.movies.repositories.protocols import MovieRepository, UserRepository

from .dependencies import movie_repo, user_movie_service, user_repo
from .models import User
from .services.protocols import UserMovieService

router = APIRouter()


UserMovieServiceDependence: TypeAlias = Annotated[UserMovieService, Depends(user_movie_service)]
UserRepoDependence: TypeAlias = Annotated[UserRepository, Depends(user_repo)]
MoviesRepoDependence: TypeAlias = Annotated[MovieRepository, Depends(movie_repo)]


@router.get('/movie/{movie_id}/rating')
async def get_movie_rating(movie_id: str, repo: MoviesRepoDependence):
    rating = await repo.rating(movie_id)
    return JSONResponse({'rating': rating}, status_code=status.HTTP_200_OK)


@router.post('/movie/rating')
async def like_movie(
    movie_id: Annotated[str, Body(...)],
    user_id: Annotated[str, Body(...)],
    value: Annotated[int, Body(gt=0, le=10)],
    service: UserMovieServiceDependence,
):
    await service.rate_movie(user_id, movie_id, value)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_200_OK)


@router.get('/userdata/{user_id}', response_model=User, responses=DEFAULT_RESPONSES)
async def get_user_data(user_id: str, repo: UserRepoDependence):
    data = await repo.get_data(user_id)

    if data is None:
        return JSONResponse({'detail': 'User not found'}, status_code=status.HTTP_404_NOT_FOUND)
    return data


@router.get('/bookmarks/{user_id}', responses=DEFAULT_RESPONSES)
async def user_bookmarks(user_id: str, repo: UserRepoDependence):
    bookmarks = await repo.bookmarks(user_id)
    if bookmarks is None:
        return JSONResponse({'detail': 'User not found'}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse({'bookmarks': bookmarks}, status_code=status.HTTP_200_OK)


@router.post('/bookmarks')
async def add_to_bookmarks(
    user_id: Annotated[str, Body(...)],
    movie_id: Annotated[str, Body(...)],
    repo: UserRepoDependence,
):
    await repo.add_bookmark(user_id, movie_id)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_201_CREATED)


@router.delete('/bookmarks')
async def remove_from_bookmarks(
    user_id: Annotated[str, Body(...)],
    movie_id: Annotated[str, Body(...)],
    repo: UserRepoDependence,
):
    try:
        await repo.remove_bookmark(user_id, movie_id)
    except EntityDoesNotExist as e:
        return JSONResponse({'detail': str(e)}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_202_ACCEPTED)


@router.post('/reviews')
async def add_review(
    movie_id: Annotated[str, Body(...)],
    user_id: Annotated[str, Body(...)],
    text: Annotated[str, Body(...)],
    service: UserMovieServiceDependence,
):
    try:
        await service.add_review(user_id, movie_id, text)
    except EntityAlreadyExists as e:
        return JSONResponse({'detail': str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_201_CREATED)


@router.put('/reviews')
async def update_review(
    movie_id: Annotated[str, Body(...)],
    user_id: Annotated[str, Body(...)],
    text: Annotated[str, Body(...)],
    service: UserMovieServiceDependence,
):
    try:
        await service.update_review(user_id, movie_id, text)
    except EntityDoesNotExist as e:
        return JSONResponse({'detail': str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_202_ACCEPTED)


@router.delete('/reviews', responses=DEFAULT_RESPONSES)
async def delete_review(
    movie_id: Annotated[str, Body(...)],
    user_id: Annotated[str, Body(...)],
    service: UserMovieServiceDependence,
):
    try:
        await service.delete_review(user_id, movie_id)
    except EntityDoesNotExist as e:
        return JSONResponse({'detail': str(e)}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_202_ACCEPTED)
