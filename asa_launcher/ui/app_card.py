"""Reusable application-card component."""

from __future__ import annotations

from nicegui import ui

from asa_launcher.registry import Application, AppStatus


_STATUS_PRESENTATION = {
    AppStatus.AVAILABLE: ("Available", "status-available", "Open app"),
    AppStatus.UNAVAILABLE: ("Unavailable", "status-unavailable", "Unavailable"),
    AppStatus.COMING_SOON: ("Coming soon", "status-coming-soon", "Coming soon"),
}


def create_app_card(application: Application) -> None:
    """Render one registry-backed launcher card."""
    status_label, status_class, button_label = _STATUS_PRESENTATION[application.status]

    with ui.element("article").classes("app-card"):
        with ui.element("div").classes("app-card-top"):
            with ui.element("div").classes("app-icon"):
                ui.icon(application.icon)
            ui.label(status_label).classes(f"status-badge {status_class}")

        ui.label(application.name).classes("app-name")
        ui.label(application.description).classes("app-description")

        if application.status is AppStatus.AVAILABLE and application.url:
            ui.button(
                button_label,
                icon="open_in_new",
                on_click=lambda: ui.navigate.to(application.url, new_tab=True),
            ).props("unelevated no-caps").classes("launch-button")
        else:
            ui.button(button_label).props("unelevated no-caps disable").classes(
                "launch-button"
            )

