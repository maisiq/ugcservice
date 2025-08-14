import logging
import time


class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[1;31m'  # Bold Red
    }
    RESET = '\033[0m'

    def format(self, record: logging.LogRecord):
        color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


class SamplerFilter(logging.Filter):
    def __init__(self, interval_sec=1, first=5, thereafter=10):
        super().__init__()
        self.interval_sec = interval_sec
        self.first = first
        self.thereafter = thereafter
        self.last_tick = time.time()
        self.counter = 0

    def filter(self, record):
        now = time.time()
        if now - self.last_tick > self.interval_sec:
            self.last_tick = now
            self.counter = 0
        self.counter += 1
        return self.counter <= self.first or self.counter % self.thereafter == 0


color_formatter = ColorFormatter()
sampler_filter = SamplerFilter()
