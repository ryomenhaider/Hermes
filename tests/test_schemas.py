import polars as pl
import pytest

import hermes as hr
from hermes.core.errors import SchemaError
from hermes.schemas.base import FieldDef, Schema
from hermes.schemas.registry import SchemaRegistry

EXPECTED_NAMES = [
    "document",
    "economic.observation",
    "entity",
    "financial.observation",
    "geopolitical.event",
    "market.observation",
    "security.event",
]


def test_canonical_registry_seeded():
    registry = SchemaRegistry()
    assert registry.list_names() == EXPECTED_NAMES
    assert registry.get("company").name == "entity"
    for name in EXPECTED_NAMES:
        assert registry.get(name) is not None
        assert registry.get(name).namespace


def test_get_picks_latest_version():
    def schema(version):
        return Schema(
            name="x",
            version=version,
            fields=[FieldDef(name="a", type="str", required=True)],
        )

    registry = SchemaRegistry(seed=False)
    registry.register(schema("1.0.0"))
    registry.register(schema("1.1.0"))
    assert registry.get("x").version == "1.1.0"
    assert registry.get("x", "1.0.0").version == "1.0.0"
    with pytest.raises(SchemaError):
        registry.register(Schema(name="x", version="1.0.0", fields=[]))


def test_validate_data_reports_violations():
    registry = SchemaRegistry(seed=False)
    registry.register(
        Schema(
            name="x",
            version="1.0.0",
            fields=[
                FieldDef(name="id", type="str", required=True),
                FieldDef(name="value", type="float", nullable=True),
            ],
            primary_keys=["id"],
        )
    )
    schema = registry.get("x")
    assert schema.validate_data(pl.DataFrame({"id": ["a"], "value": [1.5]})) == []
    violations = schema.validate_data(pl.DataFrame({"id": [None], "value": [1.5]}))
    assert any("nulls" in v for v in violations)


def test_compare_and_migrate():
    registry = SchemaRegistry()
    old = registry.get("economic.observation")
    new = Schema(
        name="economic.observation",
        version="1.1.0",
        fields=old.fields + [FieldDef(name="region", type="str", nullable=True)],
        primary_keys=old.primary_keys,
        description=old.description,
    )
    outcome = registry.compare(old, new)
    assert outcome.compatible
    frame = pl.DataFrame(
        {
            "entity_id": ["HRM-ENTITY-AAA"],
            "date": ["2024-01-01"],
            "indicator": ["CPI"],
            "value": [3.5],
            "unit": ["score"],
            "frequency": ["A"],
            "source": ["test"],
        }
    )
    migrated = registry.migrate(frame, "economic.observation", new)
    assert migrated.columns == new.field_names()

    with pytest.raises(SchemaError):
        registry.migrate(frame, "document", "entity")


def test_hr_schema_api_results():
    result = hr.get_schema("market.observation")
    assert result.is_success()
    assert result.data.name == "market.observation"

    missing = hr.get_schema("nope")
    assert not missing.is_success()
    assert missing.errors[0].code == "SchemaError"

    ok = hr.compare_schema("economic.observation", "economic.observation")
    assert ok.is_success() and ok.data.compatible

    migrated = hr.migrate(
        pl.DataFrame({"a": [1], "b": [2]}),
        Schema(name="from", version="1", fields=[FieldDef(name="a", type="integer"), FieldDef(name="b", type="integer", nullable=True)]),
        Schema(name="to", version="2", fields=[FieldDef(name="a", type="integer")]),
    )
    assert migrated.is_success()
    assert migrated.data.columns == ["a"]