from hermes.core.errors import SchemaError
from hermes.core.result import Result
from hermes.schemas.base import Schema
from hermes.schemas.registry import SchemaRegistry, get_registry


def _registry() -> SchemaRegistry:
    return get_registry()


def get_schema(name: str, version: str | None = None) -> Result:
    schema = _registry().get(name, version)
    if schema is None:
        r = Result(status="failure")
        r.add_error(SchemaError(f"Unknown schema {name!r}"))
        return r
    stats = {"namespace": schema.namespace, "version": schema.version, "fields": len(schema.fields)}
    return Result(status="success", data=schema, statistics=stats)


def register_schema(schema: object) -> Result:
    if not isinstance(schema, Schema):
        r = Result(status="failure")
        r.add_error(SchemaError(f"Expected Schema, got {type(schema).__name__}"))
        return r
    try:
        _registry().register(schema)
    except SchemaError as exc:
        r = Result(status="failure")
        r.add_error(exc)
        return r
    return Result(status="success", data=schema, statistics={"name": schema.name, "version": schema.version})


def compare_schema(schema_a: object, schema_b: object) -> Result:
    try:
        outcome = _registry().compare(schema_a, schema_b)
    except SchemaError as exc:
        r = Result(status="failure")
        r.add_error(exc)
        return r
    return Result(status="success", data=outcome, statistics={"compatible": outcome.compatible})


def migrate(data: object, from_schema: object, to_schema: object, *, rename: dict | None = None) -> Result:
    try:
        frame = _registry().migrate(data, from_schema, to_schema, rename=rename)
    except SchemaError as exc:
        r = Result(status="failure")
        r.add_error(exc)
        return r
    return Result(status="success", data=frame)