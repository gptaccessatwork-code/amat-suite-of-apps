"""Logging setup with console output and a bounded application log."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def configure_logging(level_name: str, log_file: Path) -> None:
    """Configure process-wide logging, retaining console output if file I/O fails."""
    level = getattr(logging, level_name, logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    handlers: list[logging.Handler] = [console_handler]
    file_error: OSError | None = None

    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=2_000_000,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    except OSError as error:
        file_error = error

    logging.basicConfig(level=level, handlers=handlers, force=True)
    if file_error is not None:
        logging.getLogger(__name__).warning("File logging is unavailable: %s", file_error)
