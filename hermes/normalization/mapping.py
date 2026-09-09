from collections.abc import Callable

from pydantic import BaseModel


class FieldMapping(BaseModel):
    source_field: str
    target_field: str
    transform: Callable | None = None
    dtype: str | None = None
    default: object = None
