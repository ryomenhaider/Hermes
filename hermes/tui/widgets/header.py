from textual.app import ComposeResult
from textual.widgets import Header


class HermesHeader(Header):
    def on_mount(self) -> None:
        self.title = "Hermes"
        self.sub_title = "Universal Data Acquisition Platform"
