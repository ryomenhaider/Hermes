from hermes.core.errors import UnknownEntityTypeError
from hermes.entities.models import Entity
from hermes.entities.resolver import Resolver


class EntityRegistry:
    """Resolvers keyed by entity type; population happens outside core."""

    def __init__(self) -> None:
        self._resolvers: dict[str, Resolver] = {}

    def register(self, entity_type: str, resolver: Resolver) -> None:
        self._resolvers[entity_type.lower()] = resolver

    def get(self, entity_type: str) -> Resolver | None:
        return self._resolvers.get(entity_type.lower())

    def resolve(self, query: str, entity_type: str | None = None) -> Entity | None:
        if entity_type is None:
            for resolver in self._resolvers.values():
                hit = resolver.resolve(query)
                if hit is not None:
                    return hit
            return None
        resolver = self.get(entity_type)
        if resolver is None:
            raise UnknownEntityTypeError(f"No resolver registered for entity type {entity_type!r}")
        return resolver.resolve(query)

    def list_types(self) -> list[str]:
        return sorted(self._resolvers)


__all__ = ["EntityRegistry"]