from datetime import datetime

from pydantic import BaseModel, Field


class DataVersion(BaseModel):
    content_hash: str
    schema_hash: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    parent_version: str | None = None

    def is_compatible(self, other: "DataVersion") -> bool:
        if self.schema_hash is None or other.schema_hash is None:
            return False
        return self.schema_hash == other.schema_hash
