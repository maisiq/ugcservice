from aiokafka import AIOKafkaProducer, errors
from src.logger.logger import get_logger


async def publish_message(producer: AIOKafkaProducer, topic: str, message: bytes, raise_on_err: bool = True):
    logger = get_logger()
    try:
        logger.debug(f'publish_message(): Add the message ({message}) to the buffer')
        await producer.send_and_wait(topic, message)
        logger.debug('publish_message(): Message is acknowledged')
    except (
        errors.UnknownTopicOrPartitionError,
        errors.KafkaTimeoutError,
        errors.LeaderNotAvailableError,
    ) as e:
        logger.error("publish_message(): %s", e)
        if raise_on_err:
            raise
    else:
        return True
    return False
