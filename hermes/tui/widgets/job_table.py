from __future__ import annotations

from typing import Any
from textual.app import ComposeResult
from textual.widgets import DataTable
from textual.widget import Widget


class JobTable(Widget):
    """Data table widget for displaying job history."""

    def compose(self) -> ComposeResult:
        yield DataTable(id="job-table")

    def on_mount(self) -> None:
        table = self.query_one("#job-table", DataTable)
        table.add_columns("ID", "Source", "Status", "Rows", "Runtime", "Timestamp")

    def populate(self, jobs: list[dict[str, Any]]) -> None:
        table = self.query_one("#job-table", DataTable)
        table.clear()
        for job in jobs:
            table.add_row(
                str(job["id"]),
                job.get("source_id", ""),
                job.get("status", ""),
                str(job.get("rows", 0)),
                f"{job.get('runtime', 0):.1f}s",
                job.get("timestamp", ""),
            )

    def get_selected_job_id(self) -> int | None:
        table = self.query_one("#job-table", DataTable)
        row = table.cursor_row
        if row is not None:
            try:
                return int(table.get_row_at(row)[0])
            except (IndexError, ValueError):
                pass
        return None
