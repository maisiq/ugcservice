import asyncio
import logging

from aiokafka import AIOKafkaConsumer
import clickhouse_connect
from pydantic import ValidationError

from config import kafka_config, ch_config, Topics
from models import AnalyticEvent

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def load_data(data: dict):
    ch_client = await clickhouse_connect.get_async_client(
        host=ch_config.HOST,
        port=ch_config.PORT,
        username=ch_config.USER,
        password=ch_config.PASSWORD,
    )
    result = await ch_client.insert(ch_config.ANALYTICS_TABLE, [list(data.values())], list(data.keys()))
    logger.debug(result.summary)


def deserializer(data: bytes) -> dict:
    event = AnalyticEvent.model_validate_json(data)
    return event.model_dump()


async def consume():
    consumer = AIOKafkaConsumer(
        *[t.value for t in Topics],
        bootstrap_servers=kafka_config.BOOTSTRAP_SERVERS,
        group_id=kafka_config.CONSUMER_GROUP_ID,
        enable_auto_commit=False,
    )
    async with consumer as c:
        async for msg in c:
            logger.debug("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
            try:
                data = deserializer(msg.value)
            except ValidationError as e:
                logger.error(e)
            else:
                await load_data(data)
                await consumer.commit()


asyncio.run(consume())
