from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd
from sqlalchemy import MetaData, Table, column, inspect, select, text

from hermes.database import SyncDatabase


DTYPE_MAP = {
    "int64": "BIGINT",
    "int32": "INTEGER",
    "int16": "SMALLINT",
    "int8": "SMALLINT",
    "float64": "DOUBLE PRECISION",
    "float32": "REAL",
    "object": "TEXT",
    "string": "TEXT",
    "bool": "BOOLEAN",
    "datetime64[ns]": "TIMESTAMPTZ",
    "datetime64[ns, UTC]": "TIMESTAMPTZ",
    "category": "TEXT",
}


class FeatureStore:
    def __init__(self, db: SyncDatabase):
        self._db = db

    def store(
        self,
        df: pd.DataFrame,
        feature_set: str,
        version: int | None = None,
        description: str = "",
    ) -> int:
        table_name = f"features_{feature_set}"
        self._ensure_table(table_name, df)
        self._ensure_registry_table()

        if version is None:
            version = self._next_version(table_name)

        df = df.copy()
        df["_version"] = version
        df["_created_at"] = datetime.now(timezone.utc)

        self._db.insert(table_name, df.to_dict(orient="records"))

        self._db.upsert(
            "_feature_sets",
            [{
                "name": feature_set,
                "table_name": table_name,
                "latest_version": version,
                "description": description,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }],
            conflict_columns=["name"],
        )

        return version

    def load(
        self,
        feature_set: str,
        version: int | None = None,
        filters: dict[str, Any] | None = None,
    ) -> pd.DataFrame:
        table_name = f"features_{feature_set}"

        cols = [c for c in self._columns(table_name) if c not in ("_version", "_created_at")]
        filter_dict: dict[str, Any] = dict(filters or {})

        if version is not None:
            filter_dict["_version"] = version

        batches = list(self._db.read(table_name, filters=filter_dict or None, columns=cols))

        if not batches:
            return pd.DataFrame()

        rows = []
        for batch in batches:
            rows.extend(batch)

        return pd.DataFrame(rows)

    def list_feature_sets(self) -> list[dict[str, Any]]:
        self._ensure_registry_table()
        try:
            batches = list(self._db.read("_feature_sets"))
            rows = []
            for batch in batches:
                rows.extend(batch)
            return rows
        except Exception:
            return []

    def delete(self, feature_set: str, version: int | None = None) -> int:
        table_name = f"features_{feature_set}"

        if version is None:
            self._db.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            self._db.delete("_feature_sets", {"name": feature_set})
            return -1

        result = self._db.delete(table_name, {"_version": version})
        current = self._db.read("_feature_sets", {"name": feature_set})
        latest = list(current)
        if latest and latest[0][0].get("latest_version") == version:
            remaining = list(self._db.read(table_name, columns=["_version"], batch_size=1))
            if not remaining:
                self._db.delete("_feature_sets", {"name": feature_set})
            else:
                new_ver = max(r["_version"] for batch in remaining for r in batch)
                self._db.update("_feature_sets", {"name": feature_set}, {"latest_version": new_ver})
        return result

    def _ensure_table(self, table_name: str, df: pd.DataFrame) -> None:
        inspector = inspect(self._db._engine)
        if inspector.has_table(table_name):
            return

        cols = []
        for col_name, dtype in df.dtypes.items():
            sql_type = DTYPE_MAP.get(str(dtype), "TEXT")
            safe = col_name.replace("'", "''")
            cols.append(f"    {safe} {sql_type}")

        cols.append("    _version INTEGER NOT NULL DEFAULT 1")
        cols.append("    _created_at TIMESTAMPTZ DEFAULT NOW()")

        col_list = ", ".join(c.split("    ")[1] for c in cols[:-2])
        pk = ", ".join(df.columns[:3]) if len(df.columns) >= 3 else ", ".join(df.columns)
        pk = f"{pk}, _version"

        sql = f"""
            CREATE TABLE {table_name} (
                {', '.join(cols)},
                PRIMARY KEY ({pk})
            )
        """
        self._db.execute(text(sql))

    def _ensure_registry_table(self) -> None:
        self._db.execute(text("""
            CREATE TABLE IF NOT EXISTS _feature_sets (
                name            TEXT PRIMARY KEY,
                table_name      TEXT NOT NULL,
                latest_version  INTEGER NOT NULL DEFAULT 1,
                description     TEXT DEFAULT '',
                updated_at      TEXT
            )
        """))

    def _next_version(self, table_name: str) -> int:
        try:
            rows = list(self._db.read(table_name, columns=["_version"],
                                      order_by="_version DESC", limit=1))
            for batch in rows:
                for r in batch:
                    return r["_version"] + 1
        except Exception:
            pass
        return 1

    def _columns(self, table_name: str) -> list[str]:
        inspector = inspect(self._db._engine)
        return [c["name"] for c in inspector.get_columns(table_name)]
