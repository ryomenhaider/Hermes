ALIASES: dict[str, list[str]] = {}


def add_alias(entity_id: str, alias: str) -> None:
    raise NotImplementedError()


def resolve_alias(alias: str) -> str | None:
    raise NotImplementedError()


def list_aliases(entity_id: str) -> list[str]:
    raise NotImplementedError()
