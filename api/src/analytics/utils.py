from aiokafka import AIOKafkaProducer

from .config import kafka_config


async def send_one(topic: str, message: bytes):
    producer = AIOKafkaProducer(
        bootstrap_servers=kafka_config.BOOTSTRAP_SERVERS,
    )
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        result = await producer.send_and_wait(topic, message)
        print(result)
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()
