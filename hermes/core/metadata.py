from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from hermes.core.lineage import Lineage
from hermes.core.provenance import Provenance


@dataclass
class ColumnMetadata:
    name: str
    dtype: str
    null_count: int = 0
    null_ratio: float = 0.0
    unique_count: int = 0
    min_value: Any | None = None
    max_value: Any | None = None
    mean: float | None = None
    median: float | None = None
    std: float | None = None
    top_values: list[tuple[Any, Any]] = field(default_factory=list)


@dataclass
class QualityInfo:
    completeness: dict[str, float] = field(default_factory=dict)
    duplicate_count: int = 0
    anomaly_count: dict[str, int] = field(default_factory=dict)


@dataclass
class MetaData:
    row_count: int = 0
    column_count: int = 0
    columns: list[ColumnMetadata] = field(default_factory=list)
    date_range: dict[str, tuple[Any, Any]] | None = None
    frequency: str | None = None
    source: str | None = None
    retrieved_at: datetime | None = None
    profiled_at: datetime | None = None
    quality: QualityInfo | None = None
    deep_stats: bool = True


@dataclass
class InspectReport:
    dataset_id: str | None = None
    name: str | None = "dataset"
    version: str | None = None
    schema_ref: str | None = None

    row_count: int | None = None
    column_count: int | None = None

    columns: list[tuple[str, str]] = field(default_factory=list)

    stored_metadata: MetaData | None = None
    provenance: Provenance | None = None
    lineage: Lineage | None = None

    sample: list[dict[Any, Any]] = field(default_factory=list)
