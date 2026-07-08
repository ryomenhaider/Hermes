from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static, Button

from hermes.tui.widgets.header import HermesHeader
from hermes.tui.widgets.footer import HermesFooter


class JobDetailScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def __init__(self, job_id: int) -> None:
        super().__init__()
        self._job_id = job_id

    def compose(self) -> ComposeResult:
        yield HermesHeader()
        with Vertical(id="job-detail-container"):
            yield Static(f"Job #{self._job_id}", id="job-detail-title")
            yield Static("", id="job-detail-content")
            with Horizontal():
                yield Button("Back", id="back-btn")
        yield HermesFooter()

    def on_mount(self) -> None:
        job = self.app.job_manager.get(self._job_id)  # type: ignore[attr-defined]
        if job:
            lines = [
                f"Source:      {job.get('source_id', '-')}",
                f"Status:      {job.get('status', '-')}",
                f"Rows:        {job.get('rows', 0)}",
                f"Runtime:     {job.get('runtime', 0):.1f}s",
                f"Timestamp:   {job.get('timestamp', '-')}",
                f"Error:       {job.get('error', 'None')}",
                "",
                "Parameters:",
            ]
            for k, v in job.get("params", {}).items():
                lines.append(f"  {k}: {v}")
            self.query_one("#job-detail-content", Static).update("\n".join(lines))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-btn":
            self.app.pop_screen()
