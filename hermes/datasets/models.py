from pydantic import BaseModel, Field


class DatasetDescriptor(BaseModel):
    id: str
    name: str
    description: str = ""
    source: str = ""
    schema_name: str | None = Field(default=None, alias="schema")
    coverage: str | None = None
    frequency: str | None = None
    version: str = "0.0.1"
    quality: str | None = None
