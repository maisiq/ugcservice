import logging
import sys

from src.config.config import LOGGER_LEVEL

from .formatters import ColorFormatter

_global_logger: logging.Logger | None = None


def init_logger():
    global _global_logger

    logger = logging.getLogger('main')
    log_level = logging.getLevelNamesMapping().get(LOGGER_LEVEL)
    logger.setLevel(log_level)

    color_formatter = ColorFormatter()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(color_formatter)
    console_handler.setLevel(log_level)

    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    _global_logger = logger


def get_logger() -> logging.Logger:
    if _global_logger is None:
        raise RuntimeError('Logger not initialized')
    return _global_logger
