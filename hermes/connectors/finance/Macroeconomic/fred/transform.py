import logging
from typing import Any

logger = logging.getLogger(__name__)


class FredTransformer:

    def transform(
        self,
        data: list[dict[str, Any]],
        endpoint: str,
    ) -> list[dict[str, Any]]:
        if endpoint == "metadata":
            return self._transform_metadata(data)
        if endpoint == "observations":
            return self._transform_observations(data)
        raise ValueError(f"Unknown endpoint: {endpoint}")

    def _transform_metadata(
        self,
        data: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        ...

    def _transform_observations(
        self,
        data: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        ...
