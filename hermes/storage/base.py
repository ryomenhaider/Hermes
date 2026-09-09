from abc import ABC, abstractmethod


class StorageBackend(ABC):
    @abstractmethod
    def save(self, dataset: object, path: str) -> None: ...

    @abstractmethod
    def load(self, path: str) -> object: ...

    @abstractmethod
    def delete(self, path: str) -> None: ...

    @abstractmethod
    def exists(self, path: str) -> bool: ...

    @abstractmethod
    def list(self, prefix: str = "") -> list[str]: ...
