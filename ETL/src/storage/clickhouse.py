import backoff
import clickhouse_connect
from clickhouse_connect.driver import exceptions
from src.config.clickhouse import ch_config
from src.logger import get_logger
from src.utils.utils import service_down_handler


@backoff.on_exception(
    backoff.expo,
    exceptions.OperationalError,
    max_tries=5,
    max_time=10,
    on_giveup=service_down_handler,
    raise_on_giveup=True,
)
async def get_ch_client():
    logger = get_logger()

    try:
        ch_client = await clickhouse_connect.get_async_client(
            host=ch_config.HOST,
            port=ch_config.PORT,
            username=ch_config.USER,
            password=ch_config.PASSWORD,
        )
        return ch_client
    except exceptions.OperationalError as e:
        logger.error("Error with: %s", e)
        raise
