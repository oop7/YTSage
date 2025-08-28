"""
YTSage centralized logging with loguru.

- This module provides centralized logging configuration for the entire YTSage application.
- Two log files: ytsage.log (all logs) & ytsage_error.log (errors only).
"""

import sys

from loguru import logger

from src.utils.ytsage_constants import APP_LOG_DIR

# Separate configs for each handler
CONSOLE_CONFIG = {
    "sink": sys.stdout if sys.stdout else sys.stderr,
    "level": "INFO",
    "colorize": True,
    "enqueue": True,
}

ALL_LOGS_CONFIG = {
    "sink": APP_LOG_DIR / "ytsage.log",
    "level": "DEBUG",
    "rotation": "10 MB",
    "retention": "14 days",
    "compression": "zip",
    "enqueue": True,
}

ERROR_LOGS_CONFIG = {
    "sink": APP_LOG_DIR / "ytsage_error.log",
    "level": "ERROR",
    "rotation": "5 MB",
    "retention": "30 days",
    "compression": "zip",
    "enqueue": True,
}


# Logger initialization
def init_logger() -> None:
    """Configure loguru logger using separate configs for each handler."""
    logger.remove()  # Remove default loguru handler

    logger.add(**CONSOLE_CONFIG)
    logger.add(**ALL_LOGS_CONFIG)
    logger.add(**ERROR_LOGS_CONFIG)

    logger.info("YTSage logger initialized")


init_logger()

__all__ = ["logger"]
