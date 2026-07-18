from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from hermes.database import SyncDatabase


class LineageGraph:
    def __init__(self, db: SyncDatabase):
        self._db = db
        self._ensure_table()

    def _ensure_table(self) -> None:
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS _lineage ("
            "    dataset_id      TEXT NOT NULL,"
            "    source_name     TEXT NOT NULL,"
            "    pipeline_name   TEXT NOT NULL DEFAULT '',"
            "    pipeline_ver    INTEGER NOT NULL DEFAULT 1,"
            "    input_params    TEXT DEFAULT '{}',"
            "    parent_id       TEXT,"
            "    created_at      TEXT,"
            "    PRIMARY KEY (dataset_id, source_name, created_at)"
            ")"
        )

    def record(
        self,
        dataset_id: str,
        source_name: str,
        pipeline_name: str = "",
        pipeline_version: int = 1,
        input_params: dict[str, Any] | None = None,
        parent_id: str | None = None,
    ) -> None:
        import json
        self._db.insert(
            "_lineage",
            [{
                "dataset_id": dataset_id,
                "source_name": source_name,
                "pipeline_name": pipeline_name,
                "pipeline_ver": pipeline_version,
                "input_params": json.dumps(input_params or {}),
                "parent_id": parent_id or "",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }],
        )

    def trace(self, dataset_id: str) -> list[dict[str, Any]]:
        chain: list[dict[str, Any]] = []
        current = dataset_id
        visited: set[str] = set()

        while current and current not in visited:
            visited.add(current)
            batches = list(self._db.read(
                "_lineage",
                {"dataset_id": current},
                order_by="created_at",
            ))
            rows = []
            for batch in batches:
                rows.extend(batch)

            if not rows:
                break

            chain.extend(rows)
            parent = rows[0].get("parent_id", "")
            current = parent if parent else ""

        return chain

    def sources_of(self, dataset_id: str) -> list[str]:
        entries = self.trace(dataset_id)
        sources: list[str] = []
        seen: set[str] = set()
        for e in entries:
            s = e.get("source_name", "")
            if s and s not in seen:
                seen.add(s)
                sources.append(s)
        return sources

    def graph(self, dataset_id: str) -> dict[str, Any]:
        entries = self.trace(dataset_id)
        nodes: dict[str, dict[str, Any]] = {}
        edges: list[dict[str, str]] = []

        for e in entries:
            did = e["dataset_id"]
            if did not in nodes:
                nodes[did] = {
                    "id": did,
                    "source": e.get("source_name", ""),
                    "pipeline": e.get("pipeline_name", ""),
                    "pipeline_ver": e.get("pipeline_ver", 1),
                }
            parent = e.get("parent_id", "")
            if parent:
                edges.append({"from": parent, "to": did})

        return {"nodes": list(nodes.values()), "edges": edges}
