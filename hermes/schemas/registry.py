from __future__ import annotations

import re
from functools import lru_cache

import polars as pl

from hermes.core.errors import SchemaError
from hermes.schemas.base import Compatibility, Schema, polars_type
from hermes.schemas.document import DOCUMENT
from hermes.schemas.economic import ECONOMIC_OBSERVATION
from hermes.schemas.entity import ENTITY
from hermes.schemas.financial import FINANCIAL_OBSERVATION
from hermes.schemas.geopolitical import GEOPOLITICAL_EVENT
from hermes.schemas.market import MARKET_OBSERVATION
from hermes.schemas.security import SECURITY_EVENT

CANONICAL_SCHEMAS: tuple[Schema, ...] = (
    ENTITY,
    ECONOMIC_OBSERVATION,
    FINANCIAL_OBSERVATION,
    MARKET_OBSERVATION,
    GEOPOLITICAL_EVENT,
    SECURITY_EVENT,
    DOCUMENT,
)

_SCHEMA_ALIASES = {
    "company": "entity",
    "person": "entity",
    "organization": "entity",
    "country": "entity",
}


def _parse_version(version: str) -> tuple[int, int, int]:
    parts = re.split(r"[.\-+]", version)
    nums: list[int] = []
    for part in parts[:3]:
        try:
            nums.append(int(part))
        except ValueError:
            nums.append(0)
    nums.extend([0] * (3 - len(nums)))
    return (nums[0], nums[1], nums[2])


class SchemaRegistry:
    def __init__(self, seed: bool = True) -> None:
        self._schemas: dict[str, dict[str, Schema]] = {}
        if seed:
            for schema in CANONICAL_SCHEMAS:
                self.register(schema)

    def register(self, schema: Schema) -> None:
        if not schema.name or not schema.version:
            raise SchemaError("Schema must have name and version")
        versioned = self._schemas.setdefault(schema.name, {})
        existing = versioned.get(schema.version)
        if existing is not None and existing != schema:
            raise SchemaError(f"Schema {schema.name} v{schema.version} already registered with different fields")
        versioned[schema.version] = schema

    def get(self, name: str, version: str | None = None) -> Schema | None:
        versioned = self._schemas.get(_SCHEMA_ALIASES.get(name, name))
        if not versioned:
            return None
        if version is not None:
            return versioned.get(version)
        return max(versioned.values(), key=lambda s: _parse_version(s.version))

    def list(self) -> list[Schema]:
        return [s for versioned in self._schemas.values() for s in versioned.values()]

    def list_names(self) -> list[str]:
        return sorted(self._schemas.keys())

    def compare(self, a: str | Schema, b: str | Schema) -> Compatibility:
        return self._resolve(a).compatibility(self._resolve(b))

    def migrate(
        self,
        data: pl.DataFrame | pl.LazyFrame,
        from_schema: str | Schema,
        to_schema: str | Schema,
        *,
        rename: dict[str, str] | None = None,
    ) -> pl.DataFrame | pl.LazyFrame:
        source = self._resolve(from_schema)
        target = self._resolve(to_schema)
        compat = source.compatibility(target)
        if not compat.compatible:
            raise SchemaError(f"Cannot migrate {source.name} -> {target.name}: " + "; ".join(compat.notes))
        frame = data.rename(rename) if rename else data
        keep = [f.name for f in target.fields if f.name in frame.columns]
        frame = frame.select(keep)
        for f in target.fields:
            if f.name not in frame.columns:
                frame = frame.with_columns(pl.lit(None).cast(polars_type(f.type)).alias(f.name))
        for f in target.fields:
            dtype = polars_type(f.type)
            if dtype == pl.Object or isinstance(dtype, pl.List):
                continue
            if dtype in (pl.Datetime, pl.Date) and frame.schema.get(f.name) in (pl.String, pl.Utf8):
                convert = pl.col(f.name).str.to_datetime if dtype == pl.Datetime else pl.col(f.name).str.to_date
                frame = frame.with_columns(convert(strict=False))
                continue
            # ponytail: keep the column as-is if its values resist casting
            try:
                frame = frame.with_columns(pl.col(f.name).cast(dtype, strict=False))
            except Exception:  # noqa: BLE001 - best-effort coercion
                continue
        return frame

    def _resolve(self, spec: str | Schema) -> Schema:
        if isinstance(spec, Schema):
            return spec
        schema = self.get(spec)
        if schema is None:
            raise SchemaError(f"Unknown schema {spec!r}")
        return schema


@lru_cache(maxsize=1)
def get_registry() -> SchemaRegistry:
    return SchemaRegistry()


__all__ = ["SchemaRegistry", "get_registry", "CANONICAL_SCHEMAS"]