from os import getenv

from aiokafka import AIOKafkaProducer


async def send_one(topic, message):
    producer = AIOKafkaProducer(
        bootstrap_servers=[getenv('KAFKA_SERVER0'), getenv('KAFKA_SERVER1'), getenv('KAFKA_SERVER2')],
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
