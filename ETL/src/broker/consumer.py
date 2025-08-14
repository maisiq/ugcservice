import asyncio
import contextlib

import backoff
from aiokafka import AIOKafkaConsumer, errors
from src.config.kafka import Topics, kafka_config
from src.logger.logger import get_logger
from src.utils.utils import service_down_handler

_kafka_consumer: AIOKafkaConsumer | None = None


@backoff.on_exception(
    backoff.expo,
    (errors.KafkaConnectionError, TimeoutError),
    max_tries=10,
    max_time=60,
    on_giveup=service_down_handler,
)
async def _get_started_kafka_consumer():
    global _kafka_consumer

    logger = get_logger()

    if _kafka_consumer is None:
        consumer = AIOKafkaConsumer(
            *[t.value for t in Topics],
            bootstrap_servers=kafka_config.BOOTSTRAP_SERVERS,
            group_id=kafka_config.CONSUMER_GROUP_ID,
            enable_auto_commit=False,
            request_timeout_ms=40000,
            retry_backoff_ms=5000,
            auto_offset_reset='latest',
        )
        _kafka_consumer = consumer

    try:
        await _kafka_consumer.start()
    except errors.KafkaConnectionError as e:
        logger.error("Failed to connect to Kafka cluster: %s", e)
        await asyncio.wait_for(_kafka_consumer.stop(), timeout=1)
        raise e
    return _kafka_consumer


@contextlib.asynccontextmanager
async def get_kafka_consumer():
    consumer = await _get_started_kafka_consumer()
    yield consumer
    try:
        await asyncio.wait_for(consumer.stop(), timeout=1)
    except TimeoutError:
        return
