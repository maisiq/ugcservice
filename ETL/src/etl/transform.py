from pydantic import ValidationError
from src.logger import get_logger
from src.models import AnalyticEvent


class TransformDataError(Exception):
    pass


def deserializer(data: bytes) -> dict:
    event = AnalyticEvent.model_validate_json(data)
    return event.model_dump()


def transform_data(data: bytes):
    logger = get_logger()

    try:
        serialized_data = deserializer(data)
    except ValidationError as e:
        logger.error("Failed to deserialize data: %s", e)
        raise TransformDataError('Failed to transform data') from e
    # here we can enrich data
    return serialized_data
