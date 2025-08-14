import backoff
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError
from src.config.kafka import kafka_config
from src.core.utils import service_down_handler
from src.logger.logger import get_logger

_kafka_producer: AIOKafkaProducer | None = None


@backoff.on_exception(
    backoff.expo,
    KafkaConnectionError,
    max_tries=5,
    max_time=5,
    on_giveup=service_down_handler,
)
async def init_kafka_producer():
    global _kafka_producer
    logger = get_logger()

    if _kafka_producer is not None:
        logger.error('init_kafka_producer(): Kafka producer already initialized')
        return _kafka_producer

    producer = AIOKafkaProducer(
        bootstrap_servers=kafka_config.BOOTSTRAP_SERVERS,
        request_timeout_ms=1000,
    )
    logger.debug('get_kafka_producer(): Trying to connect to Kafka cluster...')
    try:
        # Get cluster layout and initial topic/partition leadership information
        await producer.start()
    except KafkaConnectionError as e:
        logger.error('get_kafka_producer(): Failed to connect to Kafka cluster. Details: %s', e)
        raise

    logger.debug('get_kafka_producer(): Connected to Kafka cluster...')

    _kafka_producer = producer
    return _kafka_producer


def get_kafka_producer():
    if _kafka_producer is None:
        raise RuntimeError('Kafka producer is not initialized')
    return _kafka_producer
