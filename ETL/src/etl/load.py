from clickhouse_connect.driver import asyncclient, exceptions
from src.config.clickhouse import ch_config
from src.logger import get_logger


async def load_data(client: asyncclient.AsyncClient, data: dict) -> bool:
    logger = get_logger()

    try:
        await client.insert(
            ch_config.ANALYTICS_TABLE,
            data=[list(data.values())],
            column_names=list(data.keys()),
        )
        return True
    except exceptions.DatabaseError as e:
        logger.error("Failed to insert data: %s", e)

    return False
