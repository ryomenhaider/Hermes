from abc import ABC, abstractmethod

from hermes.entities.models import Entity, EntityMatch


class Resolver(ABC):
    @abstractmethod
    def resolve(self, query: str) -> Entity | None: ...

    @abstractmethod
    def identify(self, data: object) -> object: ...

    @abstractmethod
    def match(self, query: str, threshold: float = 0.8) -> list[EntityMatch]: ...
