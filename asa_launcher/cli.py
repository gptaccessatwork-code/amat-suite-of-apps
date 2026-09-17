"""Command-line entry point for validation and server startup."""

from __future__ import annotations

import argparse
from dataclasses import replace
import logging
from pathlib import Path
import sys
from typing import Sequence

from nicegui import ui

from asa_launcher import __version__
from asa_launcher.config import ConfigurationError, load_configuration
from asa_launcher.logging_config import configure_logging
from asa_launcher.registry import load_applications
from asa_launcher.web import register_web_routes


LOGGER = logging.getLogger(__name__)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ASA application launcher")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--config", type=Path, help="path to launcher JSON config")
    parser.add_argument("--host", help="override the configured listen host")
    parser.add_argument("--port", type=int, help="override the configured listen port")
    parser.add_argument(
        "--validate-config",
        action="store_true",
        help="validate configuration and exit without starting the server",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)

    try:
        configuration = load_configuration(args.config)
        settings = configuration.settings
        if args.host is not None:
            host = args.host.strip()
            if not host:
                raise ConfigurationError("--host must be a non-empty string")
            settings = replace(settings, host=host)
        if args.port is not None:
            if not 1 <= args.port <= 65535:
                raise ConfigurationError("--port must be between 1 and 65535")
            settings = replace(settings, port=args.port)
    except ConfigurationError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 2

    configure_logging(settings.log_level, settings.log_file)
    applications = load_applications(configuration.applications)
    LOGGER.info(
        "Loaded %d valid application(s) from %s",
        len(applications),
        configuration.source_path,
    )

    if args.validate_config:
        if not applications:
            LOGGER.error("Configuration contains no valid applications")
            return 2
        print(
            f"Configuration valid: {len(applications)} application(s), "
            f"launcher port {settings.port}"
        )
        return 0

    register_web_routes(applications)
    LOGGER.info(
        "Starting ASA launcher %s on %s:%d",
        __version__,
        settings.host,
        settings.port,
    )
    try:
        ui.run(
            host=settings.host,
            port=settings.port,
            reload=False,
            title="ASA | AMAT Suite of Apps",
        )
    except KeyboardInterrupt:
        LOGGER.info("ASA launcher stopped")
    return 0
