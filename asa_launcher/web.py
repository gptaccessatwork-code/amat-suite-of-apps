"""NiceGUI page and health-route registration."""

from __future__ import annotations

from nicegui import app, ui

from asa_launcher import __version__
from asa_launcher.registry import Application
from asa_launcher.ui.app_card import create_app_card
from asa_launcher.ui.layout import add_global_styles, content_container, create_header


def register_web_routes(applications: tuple[Application, ...]) -> None:
    """Register routes once during process startup."""

    @app.get("/health")
    async def health() -> dict[str, str | int]:
        return {
            "status": "ok",
            "version": __version__,
            "applications": len(applications),
        }

    @ui.page("/")
    def launcher_page() -> None:
        add_global_styles()
        create_header()

        with content_container():
            ui.label("AMAT SUITE OF APPS").classes("asa-eyebrow")
            ui.label("Your applications").classes("asa-title")
            ui.label("Choose an application below to get started.").classes("asa-lead")

            with ui.element("div").classes("asa-list-heading"):
                ui.label("Available to you")
                count = len(applications)
                noun = "application" if count == 1 else "applications"
                ui.label(f"{count} {noun}").classes("asa-count")

            if applications:
                with ui.element("section").classes("apps-grid"):
                    for application in applications:
                        create_app_card(application)
            else:
                ui.label(
                    "No applications are currently configured. "
                    "Contact your administrator."
                ).classes("empty-state")

