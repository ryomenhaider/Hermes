from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Input, Static

from hermes import credentials as cred_store
from hermes.tui.widgets.header import HermesHeader
from hermes.tui.widgets.footer import HermesFooter


class CredentialFormScreen(Screen):
    """Edit all stored credentials for a given source."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def __init__(self, source_id: str) -> None:
        super().__init__()
        self._source_id = source_id

    @property
    def _source(self) -> dict[str, Any] | None:
        return self.app.registry.get(self._source_id)  # type: ignore[attr-defined]

    def compose(self) -> ComposeResult:
        yield HermesHeader()
        src = self._source
        name = src["name"] if src else self._source_id
        with Vertical(id="cred-form-container"):
            yield Static(f"{name}", id="cred-title")
            creds = (src or {}).get("credentials", [])
            if not creds:
                yield Static("This source does not require any credentials.")
                yield Button("Back", id="back-btn")
            else:
                for c in creds:
                    yield Static(c.get("label", c["key"]), classes="param-label")
                    yield Input(
                        placeholder=f"Enter {c.get('label', c['key'])}",
                        password=True,
                        id=f"cred-{c['key']}",
                        classes="cred-input",
                    )
                with Horizontal(id="cred-buttons"):
                    yield Button("Save", id="save-btn", variant="primary")
                    yield Button("Back", id="back-btn")
                yield Static("", id="cred-message")
        yield HermesFooter()

    def on_mount(self) -> None:
        src = self._source
        if src is None:
            return
        existing = cred_store.get_credential(self._source_id, {})
        for c in src.get("credentials", []):
            key = c["key"]
            val = existing.get(key, "")
            if val:
                try:
                    self.query_one(f"#cred-{key}", Input).value = val
                except Exception:
                    pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-btn":
            self.app.pop_screen()
        elif event.button.id == "save-btn":
            self._save()

    def _save(self) -> None:
        src = self._source
        if src is None:
            return
        data: dict[str, str] = {}
        for c in src.get("credentials", []):
            key = c["key"]
            try:
                data[key] = self.query_one(f"#cred-{key}", Input).value
            except Exception:
                data[key] = ""
        cred_store.save_credential(self._source_id, data)
        self.query_one("#cred-message", Static).update("Saved")
        self.app.notify(f"Credentials saved for {self._source_id}")


class QueryNameScreen(Screen):
    """Modal-like screen to name a saved query."""

    def compose(self) -> ComposeResult:
        yield HermesHeader()
        with Vertical(id="query-name-container"):
            yield Static("Save Query As:", id="query-name-label")
            yield Input(placeholder="Query name", id="query-name-input")
            with Horizontal():
                yield Button("Save", id="save-name-btn", variant="primary")
                yield Button("Cancel", id="cancel-btn")
        yield HermesFooter()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-name-btn":
            name = self.query_one("#query-name-input", Input).value.strip()
            self.dismiss(name if name else None)
        else:
            self.dismiss(None)
