from __future__ import annotations

import builtins

from hermes.schemas.base import Schema


class SchemaRegistry:
    def __init__(self) -> None:
        self._schemas: dict[str, dict[str, Schema]] = {}

    def register(self, schema: Schema) -> None:
        raise NotImplementedError()

    def get(self, name: str, version: str | None = None) -> Schema | None:
        raise NotImplementedError()

    def list(self) -> builtins.list[Schema]:
        raise NotImplementedError()

    def list_names(self) -> builtins.list[str]:
        raise NotImplementedError()

    def migrate(self, data: object, from_schema: Schema, to_schema: Schema) -> object:
        raise NotImplementedError()
