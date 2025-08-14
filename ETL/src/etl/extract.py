import asyncio
import typing

from aiokafka import AIOKafkaConsumer, ConsumerRecord
from src.logger.logger import get_logger


async def get_raw_data(
    stop_event: asyncio.Event,
    consumer: AIOKafkaConsumer,
) -> typing.AsyncGenerator[ConsumerRecord, None]:
    logger = get_logger()
    logger.info('Looking for messages..')

    while True:
        if stop_event.is_set():
            break
        try:
            msg = await asyncio.wait_for(consumer.getone(), timeout=4)
        except TimeoutError:
            logger.debug("consume(): Timeout")
            continue

        logger.debug(
            f"consume(): {msg.topic=}, {msg.partition=}, {msg.offset=}, {msg.value=}, {msg.timestamp=}",
        )

        yield msg
