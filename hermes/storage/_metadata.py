from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

from hermes.database import SyncDatabase


@dataclass
class MetadataRecord:
    source_name: str
    indicator_id: str
    last_fetched: datetime | None = None
    row_count: int = 0
    quality_score: float = 0.0
    checksum: str = ""
    schema_ver: int = 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_name": self.source_name,
            "indicator_id": self.indicator_id,
            "last_fetched": self.last_fetched.isoformat() if self.last_fetched else None,
            "row_count": self.row_count,
            "quality_score": self.quality_score,
            "checksum": self.checksum,
            "schema_ver": self.schema_ver,
        }


class MetadataRegistry:
    def __init__(self, db: SyncDatabase):
        self._db = db
        self._ensure_table()

    def _ensure_table(self) -> None:
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS _source_registry ("
            "    source_name   TEXT NOT NULL,"
            "    indicator_id  TEXT NOT NULL,"
            "    last_fetched  TEXT,"
            "    row_count     INTEGER NOT NULL DEFAULT 0,"
            "    quality_score REAL NOT NULL DEFAULT 0.0,"
            "    checksum      TEXT DEFAULT '',"
            "    schema_ver    INTEGER NOT NULL DEFAULT 1,"
            "    PRIMARY KEY (source_name, indicator_id)"
            ")"
        )

    def register(
        self,
        source: str,
        indicator: str,
        row_count: int = 0,
        quality_score: float = 0.0,
        checksum: str = "",
    ) -> None:
        self._db.upsert(
            "_source_registry",
            [{
                "source_name": source,
                "indicator_id": indicator,
                "last_fetched": datetime.now(timezone.utc).isoformat(),
                "row_count": row_count,
                "quality_score": quality_score,
                "checksum": checksum,
            }],
            conflict_columns=["source_name", "indicator_id"],
        )

    def update(self, source: str, indicator: str, **fields: Any) -> None:
        self._db.update(
            "_source_registry",
            {"source_name": source, "indicator_id": indicator},
            fields,
        )

    def get(self, source: str, indicator: str) -> MetadataRecord | None:
        batches = list(self._db.read(
            "_source_registry",
            {"source_name": source, "indicator_id": indicator},
        ))
        for batch in batches:
            for row in batch:
                return MetadataRecord(
                    source_name=row["source_name"],
                    indicator_id=row["indicator_id"],
                    last_fetched=(
                        datetime.fromisoformat(row["last_fetched"])
                        if row.get("last_fetched") else None
                    ),
                    row_count=row.get("row_count", 0),
                    quality_score=row.get("quality_score", 0.0),
                    checksum=row.get("checksum", ""),
                    schema_ver=row.get("schema_ver", 1),
                )
        return None

    def list(self, include_quality: bool = False) -> list[dict[str, Any]]:
        batches = list(self._db.read("_source_registry"))
        rows = []
        for batch in batches:
            for r in batch:
                entry = {
                    "source": r["source_name"],
                    "indicator": r["indicator_id"],
                    "last_fetched": r.get("last_fetched"),
                    "row_count": r.get("row_count", 0),
                }
                if include_quality:
                    entry["quality_score"] = r.get("quality_score", 0.0)
                rows.append(entry)
        return rows

    def check_freshness(self, source: str, indicator: str, max_age_hours: int = 24) -> bool:
        record = self.get(source, indicator)
        if record is None or record.last_fetched is None:
            return False
        age = datetime.now(timezone.utc) - record.last_fetched
        return age < timedelta(hours=max_age_hours)

    def staleness_report(self) -> list[dict[str, Any]]:
        now = datetime.now(timezone.utc)
        batches = list(self._db.read("_source_registry"))
        report = []
        for batch in batches:
            for r in batch:
                last = r.get("last_fetched")
                age_hours = -1
                if last:
                    last_dt = datetime.fromisoformat(last)
                    age_hours = (now - last_dt).total_seconds() / 3600
                report.append({
                    "source": r["source_name"],
                    "indicator": r["indicator_id"],
                    "age_hours": round(age_hours, 1),
                })
        return report
