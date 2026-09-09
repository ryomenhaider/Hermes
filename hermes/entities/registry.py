from hermes.entities.resolver import Resolver


class EntityRegistry:
    def __init__(self) -> None:
        self._resolvers: dict[str, Resolver] = {}

    def register(self, entity_type: str, resolver: Resolver) -> None:
        raise NotImplementedError()

    def get(self, entity_type: str) -> Resolver | None:
        raise NotImplementedError()

    def resolve(self, query: str, entity_type: str | None = None) -> object:
        raise NotImplementedError()

    def list_types(self) -> list[str]:
        raise NotImplementedError()
