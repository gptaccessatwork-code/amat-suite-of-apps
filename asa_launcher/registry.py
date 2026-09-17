"""Application registry models and validation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import logging
import re
from typing import Any, Iterable, Mapping
from urllib.parse import urlparse


LOGGER = logging.getLogger(__name__)
_APP_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


class AppStatus(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    COMING_SOON = "coming_soon"


@dataclass(frozen=True, slots=True)
class Application:
    id: str
    name: str
    description: str
    url: str | None
    status: AppStatus
    icon: str


class InvalidApplication(ValueError):
    """Raised when one application registry entry is malformed."""


def _required_text(entry: Mapping[str, Any], field: str) -> str:
    value = entry.get(field)
    if not isinstance(value, str) or not value.strip():
        raise InvalidApplication(f"{field!r} must be a non-empty string")
    return value.strip()


def _validated_url(value: Any, *, required: bool) -> str | None:
    if value in (None, "") and not required:
        return None
    if not isinstance(value, str):
        raise InvalidApplication("'url' must be a string")

    url = value.strip()
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise InvalidApplication("'url' must be an absolute HTTP or HTTPS URL")
    return url


def parse_application(entry: Mapping[str, Any]) -> Application:
    """Validate and convert one registry entry."""
    app_id = _required_text(entry, "id")
    if not _APP_ID_PATTERN.fullmatch(app_id):
        raise InvalidApplication(
            "'id' must start with a lowercase letter and contain only letters, "
            "numbers, and underscores"
        )

    try:
        status = AppStatus(entry.get("status"))
    except (TypeError, ValueError) as error:
        allowed = ", ".join(item.value for item in AppStatus)
        raise InvalidApplication(f"'status' must be one of: {allowed}") from error

    icon_value = entry.get("icon", "apps")
    icon = icon_value.strip() if isinstance(icon_value, str) else ""

    return Application(
        id=app_id,
        name=_required_text(entry, "name"),
        description=_required_text(entry, "description"),
        url=_validated_url(entry.get("url"), required=status is AppStatus.AVAILABLE),
        status=status,
        icon=icon or "apps",
    )


def load_applications(registry: Iterable[object]) -> tuple[Application, ...]:
    """Load valid entries while isolating errors to the affected application."""
    applications: list[Application] = []
    seen_ids: set[str] = set()

    for position, entry in enumerate(registry, start=1):
        try:
            if not isinstance(entry, Mapping):
                raise InvalidApplication("entry must be a JSON object")
            application = parse_application(entry)
            if application.id in seen_ids:
                raise InvalidApplication(f"duplicate application id {application.id!r}")
        except InvalidApplication as error:
            LOGGER.error("Skipping application entry %d: %s", position, error)
            continue

        seen_ids.add(application.id)
        applications.append(application)

    return tuple(applications)

