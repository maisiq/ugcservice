import asyncio
import signal
import sys

from src.logger.logger import get_logger


def service_down_handler(e):
    get_logger().error("service_down_handler: %s", e)


def signal_handler(stop_event: asyncio.Event, sig: int, *_):
    get_logger().info(f"Получен сигнал {signal.strsignal(sig)}, сворачиваемся...")
    stop_event.set()

    loop = asyncio.get_running_loop()
    # Ждем ~5с и выходим
    loop.call_later(5, sys.exit, 0)
