import logging
import sys

from src.config.config import LOGGER_LEVEL

from .config import color_formatter, sampler_filter

_global_logger: logging.Logger | None = None


def init_logger():
    global _global_logger

    logger = logging.getLogger('ETL')

    log_level = logging.getLevelNamesMapping().get(LOGGER_LEVEL)
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(color_formatter)
    console_handler.setLevel(log_level)

    logger.addHandler(console_handler)
    logger.addFilter(sampler_filter)

    _global_logger = logger


def get_logger() -> logging.Logger:
    if _global_logger is None:
        raise RuntimeError('Logger not initialized')
    return _global_logger
