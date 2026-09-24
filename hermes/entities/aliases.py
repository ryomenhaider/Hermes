ALIASES: dict[str, set[str]] = {}
ALIAS_INDEX: dict[str, str] = {}


def add_alias(entity_id: str, alias: str) -> None:
    alias = alias.strip()
    if not alias:
        return
    ALIASES.setdefault(entity_id, set()).add(alias)
    ALIAS_INDEX[alias.lower()] = entity_id


def resolve_alias(alias: str) -> str | None:
    return ALIAS_INDEX.get(alias.strip().lower())


def list_aliases(entity_id: str) -> list[str]:
    return sorted(ALIASES.get(entity_id, set()))


__all__ = ["add_alias", "resolve_alias", "list_aliases", "ALIASES", "ALIAS_INDEX"]