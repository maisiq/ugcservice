import asyncio
import functools
import signal
import sys

from src.broker.consumer import get_kafka_consumer
from src.etl.runner import run_etl
from src.logger import get_logger, init_logger
from src.storage.clickhouse import get_ch_client
from src.utils.utils import signal_handler


async def main():
    init_logger()
    logger = get_logger()
    logger.info('ETL process starting...')

    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    for sig in (signal.SIGINT, signal.SIGTERM):
        if sys.platform == 'win32':
            signal.signal(sig, functools.partial(signal_handler, stop_event))
        else:
            loop.add_signal_handler(sig, signal_handler, stop_event, sig)

    async with get_kafka_consumer() as kafka_consumer:
        ch_client = await get_ch_client()
        await asyncio.create_task(run_etl(stop_event, kafka_consumer, ch_client))
        ch_client.client.close_connections()

    logger.info('Process stopped')


if __name__ == '__main__':
    asyncio.run(main())
