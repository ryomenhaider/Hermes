from textual.app import ComposeResult
from textual.widgets import Header


class HermesHeader(Header):
    def compose(self) -> ComposeResult:
        yield Header()

    def on_mount(self) -> None:
        self.title = "Hermes"
        self.sub_title = "A universal DataPlatform"

