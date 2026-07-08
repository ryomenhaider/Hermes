from textual.app import ComposeResult
from textual.widgets import Static


class StatusBar(Static):
    """Bottom status bar showing app state."""

    def __init__(self, text: str = "Ready") -> None:
        super().__init__(text, id="status-bar")

    def set_status(self, text: str) -> None:
        self.update(text)
