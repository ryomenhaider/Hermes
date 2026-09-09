from typing import Literal

from hermes.core.errors import ConfigError

API_SOURCES = [
    'fred', 'opensanctions', 'newsdata'
]

class HermesConfig:

    def __init__(self) -> None:
        self._api_keys: dict[str, str] = {}
        self._settings: dict[str, str] = {}

    def set_api_key(self, source: str, key: str) -> None:
        self._api_keys[source] = key

    def get_api_key(self, source: str) -> str | None:
        return self._api_keys[source]

    def requires_api_key(self, source: Literal[API_SOURCES]) -> bool:
        
        req: list[str] = API_SOURCES
        
        if source in req:
            return True
        else:
            return False

    def resolve_config(self, source: str) -> dict[str, str]:
        ...


_config: HermesConfig | None = None


def configure(api_keys: dict[str, str] | None = None, **settings: str) -> HermesConfig:
    ...


def get_config() -> HermesConfig:
    ...
