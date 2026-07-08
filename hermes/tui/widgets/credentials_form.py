from __future__ import annotations

from typing import Any
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, Static, Button


class CredentialInput(Vertical):
    """Input widget for a single credential field."""

    def __init__(self, credential_def: dict[str, Any], current_value: str = "") -> None:
        super().__init__()
        self.credential_def = credential_def
        self._value = current_value

    def compose(self) -> ComposeResult:
        label = self.credential_def.get("label", self.credential_def["key"])
        yield Static(label, classes="param-label")
        yield Input(
            placeholder=f"Enter {label}",
            password=True,
            value=self._value,
            id=f"cred-{self.credential_def['key']}",
            classes="param-input",
        )

    def get_value(self) -> str:
        return self.query_one(Input).value
