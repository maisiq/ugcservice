import asyncio
import json

from aiokafka import AIOKafkaConsumer
import clickhouse_connect

from config import kafka_config, ch_config, Topics


async def load_data(data: dict):
    ch_client = await clickhouse_connect.get_async_client(
        host=ch_config.HOST,
        port=ch_config.PORT,
        username=ch_config.USER,
        password=ch_config.PASSWORD,
    )
    result = await ch_client.insert(ch_config.ANALYTICS_TABLE, [list(data.values())], list(data.keys()))
    print(result.summary)


def deserializer(data: bytes) -> dict:
    return json.loads(data)


async def consume():
    consumer = AIOKafkaConsumer(
        *[t.value for t in Topics],
        bootstrap_servers=kafka_config.BOOTSTRAP_SERVERS,
        group_id=kafka_config.CONSUMER_GROUP_ID,
        enable_auto_commit=False,
    )
    async with consumer as c:
        async for msg in c:
            print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
            data = deserializer(msg.value)
            await load_data(data)
            await consumer.commit()


asyncio.run(consume())
