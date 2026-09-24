import os
from pathlib import Path


class HermesConfig:
    def __init__(self) -> None:
        self._settings: dict[str, str] = {}

    @property
    def storage_root(self) -> str:
        """Storage root: explicit setting > HERMES_STORAGE_ROOT env var > default."""
        for value in (self._settings.get("storage_root"), os.environ.get("HERMES_STORAGE_ROOT")):
            if value:
                return value
        return str(Path.home() / ".hermes-plt" / "storage")


_config: HermesConfig | None = None


def configure(**settings: str) -> HermesConfig:
    global _config
    _config = HermesConfig()
    for key, value in settings.items():
        _config._settings[key] = value
    return _config


def get_config() -> HermesConfig:
    global _config
    if _config is None:
        _config = HermesConfig()
    return _config