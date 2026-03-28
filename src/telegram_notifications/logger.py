"""Logging configuration for the application."""

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(
    name: str,
    level: int = logging.DEBUG,
    file: bool = False,
) -> logging.Logger:
    """Return a named logger with console and optional file handler.

    Handlers are only attached once, preventing duplicate log output when
    the logger is retrieved multiple times across modules.

    Args:
        name (str): Logger name, typically `__name__` of the calling module.
        file (bool): If `True`, also writes logs to a timestamped file
            under `logs/`.
        level (int): Logging level for all handlers.
            Defaults to `logging.DEBUG`.

    Returns:
        A configured :class:`logging.Logger` instance.

    Example:
        >>> log = get_logger(__name__)
        >>> log.info("Starting scraper")

        >>> log = get_logger(__name__, file=True)
        >>> log.warning("Chat ID not found")

    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    logger.addHandler(console)

    if file:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ")
        file_handler = logging.FileHandler(log_dir / f"{timestamp}.log")
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    logger.propagate = False

    return logger
