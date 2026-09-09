from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ColumnMetadata(BaseModel):
    name: str
    dtype: str
    null_count: int = 0
    null_ratio: float = 0.0
    unique_count: int = 0
    min_value: Any = None
    max_value: Any = None


class QualityInfo(BaseModel):
    completeness: float = 0.0
    duplicate_count: int = 0
    anomaly_count: int = 0


class MetaData(BaseModel):
    row_count: int = 0
    column_count: int = 0
    columns: list[ColumnMetadata] = []
    date_range: tuple[str, str] | None = None
    frequency: str | None = None
    source: str | None = None
    retrieved_at: datetime | None = None
    quality: QualityInfo | None = None
