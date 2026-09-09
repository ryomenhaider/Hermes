from hermes.core.result import Result


def resolve_entity(query: str, entity_type: str | None = None) -> Result:
    raise NotImplementedError()


def resolve_country(query: str) -> Result:
    raise NotImplementedError()


def resolve_company(query: str) -> Result:
    raise NotImplementedError()
