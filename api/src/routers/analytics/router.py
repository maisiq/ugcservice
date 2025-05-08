from fastapi.routing import APIRouter

from .models import ViewMessage
from .utils import send_one


router = APIRouter()


@router.post('/views')
async def kafka_test(msg: ViewMessage):
    await send_one('test_topic', msg.model_dump_json().encode('utf-8'))
    return 'ok'
