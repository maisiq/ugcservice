import asyncio
import json
from os import getenv

from aiokafka import AIOKafkaConsumer
import clickhouse_connect


KAFKA_TOPICS = ['my_topic', 'test_topic']
KAFKA_CONSUMER_GROUP_ID = 'analytics'
KAFKA_BOOTSTRAP_SERVERS = [getenv('KAFKA_SERVER0'), getenv('KAFKA_SERVER1'), getenv('KAFKA_SERVER2')]
CLICKHOUSE_ANALYTICS_TABLE = 'movies.test_analytics'
CLICKHOUSE_HOST = 'clickhouse'
CLICKHOUSE_PORT = 8123


async def load_data(data: dict):
    ch_client = await clickhouse_connect.get_async_client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT)
    result = await ch_client.insert(CLICKHOUSE_ANALYTICS_TABLE, [list(data.values())], list(data.keys()))
    print(result.summary)


def deserializer(data: bytes) -> dict:
    return json.loads(data)


async def consume():
    consumer = AIOKafkaConsumer(
        *KAFKA_TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP_ID,
        enable_auto_commit=False,
    )
    async with consumer as c:
        async for msg in c:
            print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
            data = deserializer(msg.value)
            await load_data(data)
            await consumer.commit()


asyncio.run(consume())
