from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

from .models import ViewMessage
from .utils import send_one
from .config import Topics


router = APIRouter()


@router.post('/views')
async def user_movie_view_progress(msg: ViewMessage):
    await send_one(Topics.analytics, msg.model_dump_json().encode('utf-8'))
    return JSONResponse({'status': 'ok', }, status.HTTP_200_OK)
