from typing import Annotated, TypeAlias

from fastapi import Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from src.db.dependencies import movie_repo, user_repo
from src.db.exceptions import UserDoesNotExist
from src.db.repositories.protocols import MovieRepository, UserRepository
from src.services.dependencies import user_movie_service
from src.services.protocols import UserMovieService

router = APIRouter()


UserMovieServiceDependence: TypeAlias = Annotated[UserMovieService, Depends(user_movie_service)]
UserRepoDependence: TypeAlias = Annotated[UserRepository, Depends(user_repo)]
MoviesRepoDependence: TypeAlias = Annotated[MovieRepository, Depends(movie_repo)]


@router.get('/movie/{movie_id}/rating')
async def get_movie_rating(movie_id: str, repo: MoviesRepoDependence):
    resp = await repo.rating(movie_id)
    return JSONResponse(resp, status_code=status.HTTP_200_OK)


@router.post('/movie/{movie_id}/rating')
async def like_movie(movie_id: str, user_id: Annotated[int, Body(...)], service: UserMovieServiceDependence):
    await service.like(movie_id, user_id)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_200_OK)


@router.get('/userdata/{user_id}')
async def get_user_data(user_id: int, repo: UserRepoDependence):
    data = await repo.get_data(user_id)

    if data is None:
        raise HTTPException(404, 'User not found')
    return data


@router.get('/bookmarks/{user_id}')
async def user_bookmarks(user_id: int, repo: UserRepoDependence):
    return await repo.bookmarks(user_id)


@router.post('/bookmarks')
async def add_to_bookmarks(
    user_id: Annotated[int, Body(...)],
    movie_id: Annotated[str, Body(...)],
    repo: UserRepoDependence
):
    try:
        await repo.add_bookmark(user_id, movie_id)
    except UserDoesNotExist:
        return JSONResponse({'detail': 'User does not exist'}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_201_CREATED)


@router.delete('/bookmarks')
async def remove_from_bookmarks(
    user_id: Annotated[int, Body(...)],
    movie_id: Annotated[str, Body(...)],
    repo: UserRepoDependence,
):
    try:
        await repo.remove_bookmark(user_id, movie_id)
    except UserDoesNotExist:
        return JSONResponse({'detail': 'User does not exist'}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_202_ACCEPTED)


@router.post('/reviews')
async def add_review(
    movie_id: Annotated[str, Body(...)],
    user_id: Annotated[int, Body(...)],
    text: Annotated[str, Body(...)],
    service: UserMovieServiceDependence,
):
    await service.add_review(user_id, movie_id, text)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_201_CREATED)


@router.put('/reviews')
async def update_review(
    movie_id: Annotated[str, Body(...)],
    user_id: Annotated[int, Body(...)],
    text: Annotated[str, Body(...)],
    service: UserMovieServiceDependence,
):
    await service.update_review(user_id, movie_id, text)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_200_OK)


@router.delete('/reviews')
async def delete_review(
    movie_id: Annotated[str, Body(...)],
    user_id: Annotated[int, Body(...)],
    service: UserMovieServiceDependence,
):
    await service.delete_review(user_id, movie_id)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_202_ACCEPTED)
