"""Shared page shell and visual styling."""

from __future__ import annotations

from nicegui import ui


GLOBAL_CSS = """
:root {
    --asa-bg: #071522;
    --asa-surface: #102131;
    --asa-surface-hover: #13283a;
    --asa-border: #263e54;
    --asa-text: #eef4fb;
    --asa-text-soft: #d6e0ec;
    --asa-muted: #91a4ba;
    --asa-muted-dark: #71859b;
    --asa-blue: #2485d4;
    --asa-blue-bright: #52b8ff;
    --asa-blue-deep: #123f60;
    --asa-green-bg: #0d4933;
    --asa-green: #50d397;
    --asa-red-bg: #47252d;
    --asa-red: #f096a6;
}

html, body, #q-app {
    min-height: 100%;
    background: var(--asa-bg);
    color: var(--asa-text);
    font-family: Inter, "Segoe UI", Arial, sans-serif;
}

body { margin: 0; }

.asa-header {
    height: 72px;
    padding: 0;
    background: #0a1927;
    border-bottom: 1px solid var(--asa-border);
    box-shadow: none;
}

.asa-header-inner {
    width: min(1088px, calc(100% - 48px));
    height: 100%;
    margin: 0 auto;
    display: flex;
    align-items: center;
}

.asa-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.asa-logo {
    width: 36px;
    height: 36px;
    flex: 0 0 36px;
    display: grid;
    place-items: center;
    border-radius: 10px;
    background: var(--asa-blue);
    color: white;
    font-size: 11px;
    font-weight: 700;
}

.asa-brand-name {
    color: var(--asa-text);
    font-size: 14px;
    line-height: 18px;
    font-weight: 700;
}

.asa-brand-subtitle {
    color: var(--asa-muted);
    font-size: 14px;
    line-height: 19px;
}

.asa-main {
    width: min(1088px, calc(100% - 48px));
    margin: 0 auto;
    padding: 76px 0 72px;
}

.asa-eyebrow {
    margin: 0 0 10px;
    color: var(--asa-blue-bright);
    font-size: 13px;
    line-height: 18px;
    font-weight: 500;
    letter-spacing: 1.4px;
    text-transform: uppercase;
}

.asa-title {
    margin: 0;
    color: #f7faff;
    font-size: 36px;
    line-height: 44px;
    font-weight: 700;
    letter-spacing: 0;
}

.asa-lead {
    margin: 14px 0 0;
    color: var(--asa-muted);
    font-size: 16px;
    line-height: 24px;
}

.asa-list-heading {
    margin-top: 50px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: var(--asa-text-soft);
    font-size: 14px;
}

.asa-count {
    color: var(--asa-muted-dark);
    font-size: 12px;
}

.apps-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
}

.app-card {
    min-width: 0;
    min-height: 246px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    background: var(--asa-surface);
    border: 1px solid var(--asa-border);
    border-radius: 14px;
    transition: background-color 140ms ease, border-color 140ms ease;
}

.app-card:hover {
    background: var(--asa-surface-hover);
    border-color: #31536e;
}

.app-card-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
}

.app-icon {
    width: 44px;
    height: 44px;
    flex: 0 0 44px;
    display: grid;
    place-items: center;
    border-radius: 12px;
    background: var(--asa-blue-deep);
    color: var(--asa-blue-bright);
}

.app-icon .q-icon { font-size: 22px; }

.status-badge {
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 11px;
    line-height: 14px;
    font-weight: 500;
}

.status-available { background: var(--asa-green-bg); color: var(--asa-green); }
.status-unavailable { background: var(--asa-red-bg); color: var(--asa-red); }
.status-coming-soon { background: #253646; color: #9aabba; }

.app-name {
    margin: 20px 0 0;
    color: var(--asa-text-soft);
    font-size: 16px;
    line-height: 22px;
    font-weight: 700;
}

.app-description {
    margin: 10px 0 22px;
    color: var(--asa-muted);
    font-size: 14px;
    line-height: 20px;
}

.launch-button {
    width: 100%;
    min-height: 36px;
    margin-top: auto;
    border-radius: 8px;
    background: var(--asa-blue);
    color: white;
    font-size: 14px;
}

.launch-button:hover { background: #2f94e4; }
.launch-button .q-btn__content { gap: 7px; flex-direction: row-reverse; }

.launch-button.q-btn--disable {
    background: #27394a !important;
    color: #7e94a8 !important;
    opacity: 1 !important;
}

.empty-state {
    padding: 36px;
    border: 1px dashed var(--asa-border);
    border-radius: 12px;
    color: var(--asa-muted);
    text-align: center;
}

@media (max-width: 900px) {
    .apps-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 620px) {
    .asa-header-inner, .asa-main { width: min(100% - 32px, 1088px); }
    .asa-main { padding-top: 48px; }
    .asa-title { font-size: 30px; line-height: 38px; }
    .asa-list-heading { margin-top: 40px; }
    .apps-grid { grid-template-columns: minmax(0, 1fr); }
}
"""


def add_global_styles() -> None:
    ui.add_css(GLOBAL_CSS)


def create_header() -> None:
    """Render the suite branding."""
    with ui.header().classes("asa-header"):
        with ui.element("div").classes("asa-header-inner"):
            with ui.element("div").classes("asa-brand"):
                ui.label("ASA").classes("asa-logo")
                with ui.element("div"):
                    ui.label("ASA").classes("asa-brand-name")
                    ui.label("AMAT Suite of Apps").classes("asa-brand-subtitle")


def content_container():
    """Return the shared constrained content element."""
    return ui.element("main").classes("asa-main")

