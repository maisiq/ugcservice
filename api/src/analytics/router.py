from typing import Annotated

from aiokafka import AIOKafkaProducer
from fastapi import Depends, Path, status
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRouter
from src.config.kafka import Topics
from src.producer.producer import get_kafka_producer
from src.producer.publish import publish_message

from .dependencies import view_repo
from .models import View, ViewMessage
from .repository.protocols import ViewRepository

router = APIRouter(tags=['views'])


@router.post('/views')
async def user_movie_view_progress(
    msg: ViewMessage,
    repo: Annotated[ViewRepository, Depends(view_repo)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
):
    ok = await repo.add_view(msg)
    await publish_message(producer, Topics.analytics.value, msg.model_dump_json().encode('utf-8'), False)

    if ok:
        return Response(status_code=status.HTTP_200_OK)
    return JSONResponse({'detail': 'Can not save the view'}, status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/views/{user_id}', response_model=list[View])
async def get_user_movies_view_progress_list(
    user_id: str,
    repo: Annotated[ViewRepository, Depends(view_repo)],
):
    return await repo.view_list(user_id)


@router.get('/views/{user_id}/{movie_id}', response_model=View)
async def get_user_movie_view_progress(
    user_id: Annotated[str, Path(...)],
    movie_id: Annotated[str, Path(...)],
    repo: Annotated[ViewRepository, Depends(view_repo)],
):
    return await repo.get_view(user_id, movie_id)
