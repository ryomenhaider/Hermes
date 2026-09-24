from dataclasses import dataclass, field
from typing import Any

import polars as pl

from hermes.core.errors import SchemaError

_POLARS_TYPES = {
    "str": pl.String,
    "string": pl.String,
    "integer": pl.Int64,
    "int": pl.Int64,
    "float": pl.Float64,
    "double": pl.Float64,
    "boolean": pl.Boolean,
    "bool": pl.Boolean,
    "date": pl.Date,
    "datetime": pl.Datetime,
    "list": pl.List(pl.Object),
    "dict": pl.Object,
}


def polars_type(t: str):
    """Map a FieldDef type string to its polars dtype."""
    try:
        return _POLARS_TYPES[t]
    except KeyError:
        raise SchemaError(f"Unknown field type {t!r}") from None


@dataclass
class FieldDef:
    name: str
    type: str
    nullable: bool = True
    required: bool = False
    description: str | None = None
    semantic_type: str | None = None
    unit: str | None = None
    constraints: dict = field(default_factory=dict)

    def polars_type(self):
        return polars_type(self.type)


@dataclass
class Compatibility:
    compatible: bool
    notes: list[str] = field(default_factory=list)


@dataclass
class Schema:
    name: str
    version: str
    fields: list[FieldDef] = field(default_factory=list)
    primary_keys: list[str] = field(default_factory=list)
    namespace: str | None = None
    description: str | None = None

    def __post_init__(self) -> None:
        if self.namespace is None and "." in self.name:
            self.namespace = self.name.split(".")[0]

    def field_names(self) -> list[str]:
        return [f.name for f in self.fields]

    def field(self, name: str) -> FieldDef | None:
        return next((f for f in self.fields if f.name == name), None)

    def validate_data(self, data: pl.DataFrame) -> list[str]:
        """Return schema violations; an empty list means the frame conforms."""
        violations: list[str] = []
        for f in self.fields:
            if f.name not in data.columns:
                if f.required:
                    violations.append(f"missing required column {f.name!r}")
                continue
            if f.required and data[f.name].null_count():
                violations.append(f"required column {f.name!r} has nulls")
        for pk in self.primary_keys:
            if pk in data.columns and data[pk].null_count():
                violations.append(f"primary key column {pk!r} has nulls")
        return violations

    def compatibility(self, other: "Schema") -> Compatibility:
        """Whether *self* can evolve into *other* without data loss."""
        notes: list[str] = []
        compatible = True
        for f in other.fields:
            mine = self.field(f.name)
            if mine is None:
                if not f.nullable or f.required:
                    compatible = False
                    notes.append(f"new non-nullable field {f.name!r}")
                else:
                    notes.append(f"new nullable field {f.name!r}")
            elif mine.type != f.type:
                compatible = False
                notes.append(f"field {f.name!r} changes type {mine.type} -> {f.type}")
        dropped = [f.name for f in self.fields if f.name not in other.field_names()]
        if dropped:
            notes.append(f"fields dropped: {', '.join(sorted(dropped))}")
        return Compatibility(compatible=compatible, notes=notes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "namespace": self.namespace,
            "version": self.version,
            "primary_keys": list(self.primary_keys),
            "description": self.description,
            "fields": [f.__dict__.copy() for f in self.fields],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Schema":
        return cls(
            name=data["name"],
            version=data["version"],
            namespace=data.get("namespace"),
            primary_keys=list(data.get("primary_keys", [])),
            description=data.get("description"),
            fields=[FieldDef(**f) for f in data.get("fields", [])],
        )


__all__ = ["FieldDef", "Schema", "Compatibility", "polars_type"]