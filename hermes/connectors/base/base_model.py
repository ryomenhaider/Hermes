from abc import ABC, abstractmethod
from typing import Any
import pandas as pd


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
    def transform(self) -> pd.DataFrame:
        ...

    @abstractmethod
    def export(self, data: list[dict[str, Any]], destination: str) -> None:
        ...

    @abstractmethod
    def health_check(self) -> dict:
        ...

    @classmethod
    def metadata(cls) -> dict:
        return {
            "id": cls.__name__.lower().replace("connector", ""),
            "name": cls.__name__.replace("Connector", ""),
            "category": "Uncategorized",
            "subcategory": "",
            "description": "",
            "credentials": [],
            "parameters": [],
            "outputs": [],
        }
