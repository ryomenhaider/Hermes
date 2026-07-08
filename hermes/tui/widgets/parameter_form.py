from __future__ import annotations

from typing import Any
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, Select, Static
from textual.widget import Widget


class ParameterInput(Widget):
    """A labeled input for a single parameter based on metadata."""

    def __init__(self, param_def: dict[str, Any], **kwargs) -> None:
        super().__init__(**kwargs)
        self.param_def = param_def

    def compose(self) -> ComposeResult:
        label = self.param_def.get("label", self.param_def["name"])
        yield Static(label, classes="param-label")
        yield Input(
            placeholder=label,
            value=str(self.param_def.get("default", "")),
            id=f"param-{self.param_def['name']}",
            classes="param-input",
        )

    def get_value(self) -> str:
        return self.query_one(Input).value

    def set_value(self, value: str) -> None:
        self.query_one(Input).value = value


class ParameterForm(Vertical):
    """Dynamic parameter form generated from metadata."""

    def __init__(self, parameters: list[dict[str, Any]], **kwargs) -> None:
        super().__init__(**kwargs)
        self._parameters = parameters

    def compose(self) -> ComposeResult:
        yield Static("Parameters", classes="section-title")
        for param in self._parameters:
            yield ParameterInput(param)

    def get_values(self) -> dict[str, str]:
        vals: dict[str, str] = {}
        for param in self._parameters:
            name = param["name"]
            widget = self.query_one(f"#param-{name}", Input)
            vals[name] = widget.value
        return vals

    def set_values(self, values: dict[str, str]) -> None:
        for name, value in values.items():
            try:
                self.query_one(f"#param-{name}", Input).value = value
            except Exception:
                pass


class DestinationSelector(Vertical):
    """Select widget for choosing export destination."""

    def __init__(self, outputs: list[str], **kwargs) -> None:
        super().__init__(**kwargs)
        self._outputs = outputs

    def compose(self) -> ComposeResult:
        yield Static("Destination", classes="section-title")
        options = [(o, o) for o in self._outputs]
        yield Select(options, prompt="Select destination...", id="destination-select")

    def get_selected(self) -> str | None:
        widget = self.query_one("#destination-select", Select)
        val = widget.value
        return str(val) if val != Select.BLANK else None
