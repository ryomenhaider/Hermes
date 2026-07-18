from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import text


class MigrationRunner:
    def __init__(self, migrations_dir: str):
        self.migrations_dir = migrations_dir

    def apply(self, conn: Any) -> list[str]:
        self._ensure_tracking_table(conn)
        pending = self._list_pending(conn)
        filenames: list[str] = []

        for filename, filepath in pending:
            checksum = self._checksum(filepath)
            sql = open(filepath).read()
            t0 = datetime.now(timezone.utc)
            conn.execute(text(sql))
            dt = int((datetime.now(timezone.utc) - t0).total_seconds() * 1000)
            conn.execute(
                text(
                    "INSERT INTO _schema_migrations (filename, checksum, duration_ms) "
                    "VALUES (:f, :c, :d)"
                ),
                {"f": filename, "c": checksum, "d": dt},
            )
            filenames.append(filename)

        return filenames

    def _ensure_tracking_table(self, conn: Any) -> None:
        conn.execute(
            text(
                "CREATE TABLE IF NOT EXISTS _schema_migrations ("
                "    filename    TEXT NOT NULL PRIMARY KEY,"
                "    applied_at  TEXT NOT NULL DEFAULT (datetime('now')),"
                "    checksum    TEXT NOT NULL,"
                "    duration_ms INTEGER NOT NULL DEFAULT 0"
                ")"
            )
        )

    def _get_applied(self, conn: Any) -> set[str]:
        rows = conn.execute(
            text("SELECT filename FROM _schema_migrations")
        ).fetchall()
        return {r[0] for r in rows}

    def _list_pending(self, conn: Any) -> list[tuple[str, str]]:
        if not os.path.isdir(self.migrations_dir):
            return []

        entries = sorted(
            [
                e
                for e in os.scandir(self.migrations_dir)
                if e.is_file() and e.name.endswith(".sql")
            ],
            key=lambda e: e.name,
        )
        applied = self._get_applied(conn)
        return [(e.name, e.path) for e in entries if e.name not in applied]

    @staticmethod
    def _checksum(filepath: str) -> str:
        data = open(filepath, "rb").read()
        return hashlib.sha256(data).hexdigest()
