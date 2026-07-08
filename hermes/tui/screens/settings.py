from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static

from hermes import settings as app_settings
from hermes.tui.widgets.header import HermesHeader
from hermes.tui.widgets.footer import HermesFooter


class SettingsScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield HermesHeader()
        with Vertical(id="settings-container"):
            yield Static("Settings", id="settings-title")
            yield Static(f"Export Directory:  {app_settings.EXPORTS_DIR}", classes="setting-line")
            yield Static(f"Cache Directory:   {app_settings.CACHE_DIR}", classes="setting-line")
            yield Static(f"Config File:       {app_settings.CONFIG_FILE}", classes="setting-line")
            yield Static(f"Credentials File:  {app_settings.CREDENTIALS_FILE}", classes="setting-line")
            yield Static("", classes="setting-line")
            yield Static(f"Version:           0.1.0", classes="setting-line")
            yield Static(f"Data Sources:      {len(self.app.registry.source_ids)}", classes="setting-line")  # type: ignore[attr-defined]
        yield HermesFooter()
