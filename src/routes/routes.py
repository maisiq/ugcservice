from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Depends, Body, status
from fastapi.responses import JSONResponse

from src.db.repository import mongo_repo, MongoRepository, UserDoesNotExist


router = APIRouter()


@router.get('/bookmarks')
async def user_bookmarks(db: Annotated[MongoRepository, Depends(mongo_repo)]):
    return await db.get_user_bookmarks(1)


@router.patch('/bookmarks')
async def add_to_bookmarks(
    user_id: Annotated[int, Body(...)],
    movie_id: Annotated[str, Body(...)],
    db: Annotated[MongoRepository, Depends(mongo_repo)]
):
    try:
        await db.add_movie_to_user_bookmarks(user_id, movie_id)
    except UserDoesNotExist:
        return JSONResponse({'detail': 'User does not exist'}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_200_OK)


@router.patch('/bookmarks/remove')
async def remove_from_bookmarks(
    user_id: Annotated[int, Body(...)],
    movie_id: Annotated[str, Body(...)],
    db: Annotated[MongoRepository, Depends(mongo_repo)]
):
    try:
        await db.remove_movie_from_user_bookmarks(user_id, movie_id)
    except UserDoesNotExist:
        return JSONResponse({'detail': 'User does not exist'}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'status': 'ok'}, status_code=status.HTTP_200_OK)
