from __future__ import annotations

from abc import ABC, abstractmethod
from difflib import SequenceMatcher

from hermes.entities.models import Entity, EntityIdentifier, EntityMatch


class Resolver(ABC):
    """Entity lookup interface. Domain knowledge never lands in core/."""

    @abstractmethod
    def resolve(self, query: str) -> Entity | None: ...

    @abstractmethod
    def identify(self, data: object) -> object: ...

    @abstractmethod
    def match(self, query: str, threshold: float = 0.8) -> list[EntityMatch]: ...


class StaticEntityResolver(Resolver):
    """Resolves against an in-memory entity set by id, name, any identifier, or alias."""

    def __init__(self, entities: list[Entity], *, entity_type: str | None = None) -> None:
        self._entities = entities
        self._index: dict[str, Entity] = {}
        for entity in entities:
            for key in entity.lookup_keys():
                self._index.setdefault(key, entity)

    def entities(self) -> list[Entity]:
        return list(self._entities)

    def resolve(self, query: str) -> Entity | None:
        return self._index.get(query.strip().lower())

    def identify(self, data: object) -> object:
        if isinstance(data, str):
            entity = self.resolve(data)
            return [entity.id] if entity else []
        if isinstance(data, dict):
            return {key: self._entity_id(value) for key, value in data.items()}
        return []

    def match(self, query: str, threshold: float = 0.8) -> list[EntityMatch]:
        q = query.strip().lower()
        scored: dict[str, EntityMatch] = {}
        for entity in self._entities:
            if self._index.get(q) is entity:
                scored[entity.id] = EntityMatch(entity, 1.0, "exact")
        for entity in self._entities:
            ratio = SequenceMatcher(None, q, entity.canonical_name.lower()).ratio()
            if ratio >= threshold:
                best = scored.get(entity.id)
                if best is None or ratio > best.score:
                    scored[entity.id] = EntityMatch(entity, round(ratio, 3), "fuzzy")
        return sorted(scored.values(), key=lambda m: -m.score)

    def _entity_id(self, value: object) -> str | None:
        if isinstance(value, EntityIdentifier):
            value = value.value
        if isinstance(value, str):
            entity = self.resolve(value)
            return entity.id if entity else None
        return None


__all__ = ["Resolver", "StaticEntityResolver"]