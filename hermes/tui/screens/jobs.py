from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static

from hermes.tui.widgets.header import HermesHeader
from hermes.tui.widgets.footer import HermesFooter
from hermes.tui.widgets.job_table import JobTable


class JobsScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("enter", "view_detail", "View Detail"),
    ]

    def compose(self) -> ComposeResult:
        yield HermesHeader()
        with Vertical():
            yield Static("Job History", id="jobs-title")
            yield JobTable(id="job-table-widget")
        yield HermesFooter()

    def on_mount(self) -> None:
        self._refresh()

    def _refresh(self) -> None:
        jobs = self.app.job_manager.list_all()  # type: ignore[attr-defined]
        table = self.query_one("#job-table-widget", JobTable)
        table.populate(jobs)

    def action_view_detail(self) -> None:
        table = self.query_one("#job-table-widget", JobTable)
        job_id = table.get_selected_job_id()
        if job_id is not None:
            from hermes.tui.screens.job_detail import JobDetailScreen
            self.app.push_screen(JobDetailScreen(job_id=job_id))
