from __future__ import annotations

from pathlib import Path
from textual.app import App
from textual.binding import Binding

from hermes.registry import SourceRegistry
from hermes.tui.job_manager import JobManager
from hermes.tui.saved_queries import SavedQueryManager
from hermes.tui.screens.main import MainMenu


class Hermes(App):
    CSS_PATH = str(Path(__file__).parent / "styles" / "app.tcss")

    BINDINGS = []

    def __init__(self) -> None:
        super().__init__()
        self.registry = SourceRegistry()
        self.job_manager = JobManager()
        self.saved_queries = SavedQueryManager()

    def on_mount(self) -> None:
        self.registry.discover()
        self.push_screen(MainMenu())
        self.title = "Hermes"
        self.sub_title = "Universal Data Acquisition Platform"


if __name__ == "__main__":
    app = Hermes()
    app.run()
