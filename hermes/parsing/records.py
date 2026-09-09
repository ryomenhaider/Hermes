from pydantic import BaseModel


class IntermediateRecord(BaseModel):
    fields: dict[str, object] = {}
    source_format: str = ""
    raw_values: dict[str, object] = {}
