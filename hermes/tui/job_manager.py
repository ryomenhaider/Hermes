from __future__ import annotations

from datetime import datetime
from typing import Any


class JobManager:
    """In-memory job history (persisted to JSON in a future iteration)."""

    def __init__(self) -> None:
        self._jobs: list[dict[str, Any]] = []
        self._next_id: int = 1

    def create(self, source_id: str, params: dict[str, str] | None = None) -> int:
        job_id = self._next_id
        self._next_id += 1
        self._jobs.append({
            "id": job_id,
            "source_id": source_id,
            "params": params or {},
            "status": "pending",
            "rows": 0,
            "runtime": 0.0,
            "error": None,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        return job_id

    def update(self, job_id: int, **kwargs: Any) -> None:
        for job in self._jobs:
            if job["id"] == job_id:
                job.update(kwargs)
                break

    def get(self, job_id: int) -> dict[str, Any] | None:
        for job in self._jobs:
            if job["id"] == job_id:
                return job
        return None

    def list_all(self) -> list[dict[str, Any]]:
        return list(reversed(self._jobs))
