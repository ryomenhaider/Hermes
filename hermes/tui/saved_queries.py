from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from hermes.settings import HERMES_DIR


class SavedQueryManager:
    """JSON-backed saved queries stored in ~/.hermes/queries.json."""

    def __init__(self) -> None:
        self._file: Path = HERMES_DIR / "queries.json"
        self._queries: dict[str, dict[str, Any]] = self._load()

    def _load(self) -> dict[str, dict[str, Any]]:
        if self._file.exists():
            try:
                raw = self._file.read_text().strip()
                return json.loads(raw) if raw else {}
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _save(self) -> None:
        self._file.write_text(json.dumps(self._queries, indent=2))

    def list_queries(self) -> list[dict[str, Any]]:
        return [
            {"name": name, **data}
            for name, data in self._queries.items()
        ]

    def get(self, name: str) -> dict[str, Any] | None:
        return self._queries.get(name)

    def save(self, name: str, source_id: str, params: dict[str, str]) -> None:
        self._queries[name] = {
            "source_id": source_id,
            "params": params,
            "created_at": datetime.now().isoformat(),
        }
        self._save()

    def delete(self, name: str) -> bool:
        if name in self._queries:
            del self._queries[name]
            self._save()
            return True
        return False
