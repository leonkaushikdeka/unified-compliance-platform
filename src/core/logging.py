import logging
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict

import structlog
from structlog.processors import TimeStamper, add_log_level

from src.core.config import settings


def setup_logging() -> None:
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    structlog.configure(
        processors=[
            add_log_level,
            TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
            if settings.LOG_FORMAT == "json"
            else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)


@asynccontextmanager
async def request_context():
    start_time = datetime.utcnow()
    yield
    duration = (datetime.utcnow() - start_time).total_seconds()


class LoggerMixin:
    @property
    def log(self) -> structlog.stdlib.BoundLogger:
        return structlog.get_logger(self.__class__.__name__)

    def log_info(self, event: str, **kwargs: Any) -> None:
        self.log.info(event, **kwargs)

    def log_error(self, event: str, **kwargs: Any) -> None:
        self.log.error(event, **kwargs)

    def log_warning(self, event: str, **kwargs: Any) -> None:
        self.log.warning(event, **kwargs)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)


setup_logging()
