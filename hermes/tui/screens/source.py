from __future__ import annotations

import time
from typing import Any

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static, Button

from hermes.tui.widgets.header import HermesHeader
from hermes.tui.widgets.footer import HermesFooter
from hermes.tui.widgets.parameter_form import ParameterForm, DestinationSelector


class SourceScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("f5", "fetch", "Fetch"),
    ]

    def __init__(self, source_id: str) -> None:
        super().__init__()
        self._source_id = source_id

    @property
    def _source(self) -> dict[str, Any]:
        return self.app.registry.get(self._source_id)  # type: ignore[attr-defined]

    def compose(self) -> ComposeResult:
        yield HermesHeader()
        src = self._source
        if src is None:
            with Vertical(id="source-container"):
                yield Static(f"Source '{self._source_id}' not found", id="source-error")
                yield Button("Back", id="back-btn")
            yield HermesFooter()
            return
        with Vertical(id="source-container"):
            yield Static(src["name"], id="source-name")

            if not self._is_implemented(src):
                yield Static(
                    "This data source hasn't been added yet.\n"
                    "See CONTRIBUTING.md for how to add it.\n\n"
                    "Once added, this page will show the\n"
                    "parameter form dynamically.",
                    id="source-unimplemented",
                )
                yield Button("Back", id="back-btn")
                yield HermesFooter()
                return

            yield Static(src.get("description", ""), id="source-desc")

            creds = src.get("credentials", [])
            if creds:
                yield Static("Credentials", classes="section-title")
                for c in creds:
                    stored = self._check_credential(c["key"])
                    status = "✓" if stored else "✗"
                    yield Static(f"  {c['label']}: {status}", classes="cred-status")

            params = src.get("parameters", [])
            if params:
                yield ParameterForm(params, id="param-form")

            outputs = src.get("outputs", [])
            if outputs:
                yield DestinationSelector(outputs, id="dest-selector")

            with Horizontal(id="button-row"):
                yield Button("Fetch Data", id="fetch-btn", variant="primary")
                yield Button("Save Query", id="save-btn")
                yield Button("Back", id="back-btn")

            yield Static("", id="result-area")
        yield HermesFooter()

    def _is_implemented(self, src: dict[str, Any]) -> bool:
        return bool(src.get("credentials") or src.get("parameters") or src.get("outputs"))

    def _check_credential(self, key: str) -> bool:
        try:
            from hermes.credentials import get_credential
            val = get_credential(self._source_id, {}).get(key)
            return bool(val)
        except Exception:
            return False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-btn":
            self.app.pop_screen()
        elif event.button.id == "fetch-btn":
            self.action_fetch()
        elif event.button.id == "save-btn":
            self.action_save_query()

    def action_fetch(self) -> None:
        src = self._source
        params = self._get_params()
        result = self.query_one("#result-area", Static)

        result.update("Starting job...")
        job_id = self.app.job_manager.create(self._source_id, params)  # type: ignore[attr-defined]
        self.app.job_manager.update(job_id, status="running")  # type: ignore[attr-defined]

        try:
            t0 = time.time()
            connector = self._load_connector(src["id"])
            if connector:
                connector.authenticate()
                data = connector.fetch(**params)
                elapsed = time.time() - t0
                row_count = len(data) if isinstance(data, list) else 0
                destination = self._get_destination()
                if destination and data:
                    connector.export(data, destination)
                self.app.job_manager.update(  # type: ignore[attr-defined]
                    job_id, status="success", rows=row_count, runtime=elapsed,
                )
                result.update(f"Success — {row_count} rows → {destination or 'not saved'} in {elapsed:.1f}s")
            else:
                self.app.job_manager.update(job_id, status="failed", error="Connector not available")  # type: ignore[attr-defined]
                result.update("Connector not available (not yet implemented)")
        except Exception as exc:
            elapsed = time.time() - t0
            self.app.job_manager.update(job_id, status="failed", error=str(exc), runtime=elapsed)  # type: ignore[attr-defined]
            result.update(f"Failed: {exc}")

    def _get_params(self) -> dict[str, str]:
        try:
            form = self.query_one("#param-form", ParameterForm)
            return form.get_values()
        except Exception:
            return {}

    def _get_destination(self) -> str | None:
        try:
            selector = self.query_one("#dest-selector", DestinationSelector)
            return selector.get_selected()
        except Exception:
            return None

    def _load_connector(self, source_id: str) -> Any:
        try:
            src = self.app.registry.get(source_id)  # type: ignore[attr-defined]
            if src and "_connector_class" in src:
                cls = src["_connector_class"]
                return cls()
            return None
        except Exception:
            return None

    def action_save_query(self) -> None:
        from hermes.tui.screens.credential_form import QueryNameScreen
        self.app.push_screen(QueryNameScreen(), self._on_query_name)

    def _on_query_name(self, name: str | None) -> None:
        if name:
            params = self._get_params()
            self.app.saved_queries.save(name, self._source_id, params)  # type: ignore[attr-defined]
            self.app.notify(f"Query '{name}' saved")
