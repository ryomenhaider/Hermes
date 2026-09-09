from datetime import datetime

from pydantic import BaseModel, Field


class DataVersion(BaseModel):
    content_hash: str
    schema_hash: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    parent_version: str | None = None

    def is_compatible(self, other: "DataVersion") -> bool:
        raise NotImplementedError()
