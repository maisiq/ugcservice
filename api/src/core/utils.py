from typing import Never

from fastapi import HTTPException, status
from src.logger.logger import get_logger


def service_down_handler(e: Exception) -> Never:
    get_logger().error(e)
    raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail='Service temporary unavailable')
