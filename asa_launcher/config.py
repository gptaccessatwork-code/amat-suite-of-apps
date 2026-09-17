"""Load and validate deployment configuration from JSON."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any, Mapping


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "launcher.json"
VALID_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})


class ConfigurationError(ValueError):
    """Raised when launcher-level configuration cannot be used safely."""


@dataclass(frozen=True, slots=True)
class LauncherSettings:
    host: str
    port: int
    log_level: str
    log_file: Path


@dataclass(frozen=True, slots=True)
class PortalConfiguration:
    settings: LauncherSettings
    applications: tuple[object, ...]
    source_path: Path


def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ConfigurationError(f"{field!r} must be a JSON object")
    return value


def _host(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError("'launcher.host' must be a non-empty string")
    return value.strip()


def _port(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigurationError("'launcher.port' must be an integer")
    if not 1 <= value <= 65535:
        raise ConfigurationError("'launcher.port' must be between 1 and 65535")
    return value


def _log_level(value: Any) -> str:
    if not isinstance(value, str) or value.upper() not in VALID_LOG_LEVELS:
        allowed = ", ".join(sorted(VALID_LOG_LEVELS))
        raise ConfigurationError(f"'launcher.log_level' must be one of: {allowed}")
    return value.upper()


def _environment_port(value: str, name: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise ConfigurationError(f"environment variable {name} must be an integer") from error
    return _port(parsed)


def resolve_config_path(path: str | Path | None = None) -> Path:
    """Resolve CLI, environment, or default configuration paths in that order."""
    selected = path or os.getenv("ASA_CONFIG_FILE") or DEFAULT_CONFIG_PATH
    return Path(selected).expanduser().resolve()


def load_configuration(path: str | Path | None = None) -> PortalConfiguration:
    """Read launcher settings and raw application entries from a JSON file."""
    source_path = resolve_config_path(path)
    try:
        with source_path.open("r", encoding="utf-8") as config_file:
            data = json.load(config_file)
    except FileNotFoundError as error:
        raise ConfigurationError(f"configuration file not found: {source_path}") from error
    except json.JSONDecodeError as error:
        raise ConfigurationError(
            f"invalid JSON in {source_path} at line {error.lineno}, column {error.colno}"
        ) from error
    except OSError as error:
        raise ConfigurationError(f"could not read configuration file: {error}") from error

    root = _mapping(data, "configuration")
    launcher = _mapping(root.get("launcher", {}), "launcher")

    configured_host = launcher.get("host", "0.0.0.0")
    configured_port = launcher.get("port", 8000)
    configured_level = launcher.get("log_level", "INFO")

    host = _host(os.getenv("ASA_LAUNCHER_HOST", configured_host))
    port_override = os.getenv("ASA_LAUNCHER_PORT")
    port = (
        _environment_port(port_override, "ASA_LAUNCHER_PORT")
        if port_override is not None
        else _port(configured_port)
    )
    log_level = _log_level(os.getenv("ASA_LOG_LEVEL", configured_level))

    log_file_value = launcher.get("log_file", "logs/asa_launcher.log")
    if not isinstance(log_file_value, str) or not log_file_value.strip():
        raise ConfigurationError("'launcher.log_file' must be a non-empty path")
    log_file = Path(log_file_value.strip()).expanduser()
    if not log_file.is_absolute():
        log_file = source_path.parent / log_file

    applications = root.get("applications")
    if not isinstance(applications, list):
        raise ConfigurationError("'applications' must be a JSON array")

    return PortalConfiguration(
        settings=LauncherSettings(
            host=host,
            port=port,
            log_level=log_level,
            log_file=log_file.resolve(),
        ),
        applications=tuple(applications),
        source_path=source_path,
    )

