from hermes.core.result import Result


def get_schema(name: str, version: str | None = None) -> Result:
    raise NotImplementedError()


def register_schema(schema: object) -> Result:
    raise NotImplementedError()


def compare_schema(schema_a: object, schema_b: object) -> Result:
    raise NotImplementedError()


def migrate(data: object, from_schema: object, to_schema: object) -> Result:
    raise NotImplementedError()
