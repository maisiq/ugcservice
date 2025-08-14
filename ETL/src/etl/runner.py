import asyncio

from aiokafka import AIOKafkaConsumer, errors
from clickhouse_connect.driver.asyncclient import AsyncClient
from src.logger.logger import get_logger

from .extract import get_raw_data
from .load import load_data
from .transform import TransformDataError, transform_data


async def run_etl(stop_event: asyncio.Event, kafka_consumer: AIOKafkaConsumer, ch_client: AsyncClient):
    logger = get_logger()

    async for msg in get_raw_data(stop_event, kafka_consumer):
        try:
            data = transform_data(msg.value)
        except TransformDataError:
            logger.error('Invalid data (%s) with offset = %s', msg.value, msg.offset)
            # save offset in dead-message-topic e.g.
            continue

        if not await load_data(ch_client, data):
            logger.error('Failed to load data with offset = %s, continue..', msg.offset)
            # save offset in dead-message-topic e.g.
            continue

        try:
            await asyncio.wait_for(kafka_consumer.commit(), timeout=1)
        except (errors.CommitFailedError, TimeoutError) as e:
            logger.error("Commit failed: %s", str(e))
            continue
        logger.debug('consume(): Offset commited;')
