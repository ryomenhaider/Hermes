from abc import ABC, abstractmethod
from typing import Any


class Connector(ABC):

    @abstractmethod
    def authenticate(self) -> bool:
        ...

    @abstractmethod
    def validate_credentials(self) -> bool:
        ...

    @abstractmethod
    def fetch(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def validate(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def transform(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def export(self, data: list[dict[str, Any]], destination: str) -> None:
        ...

    @abstractmethod
    def health_check(self) -> bool:
        ...
