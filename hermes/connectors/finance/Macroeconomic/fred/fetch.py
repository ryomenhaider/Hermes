import httpx
import logging
from typing import Any, Literal

from hermes.config import FRED_API

logger = logging.getLogger(__name__)


class FredClient:

    def __init__(self):
        self._api = FRED_API

    def get_url(
        self,
        series_id: str,
        endpoint: Literal["metadata", "observations"] = "metadata",
    ) -> str:
        if endpoint == "metadata":
            return (
                f"https://api.stlouisfed.org/fred/series"
                f"?series_id={series_id}"
                f"&api_key={self._api}"
                f"&file_type=json"
            )

        if endpoint == "observations":
            return (
                f"https://api.stlouisfed.org/fred/series/observations"
                f"?series_id={series_id}"
                f"&api_key={self._api}"
                f"&file_type=json"
            )

        raise ValueError(f"Unsupported endpoint: {endpoint}")

    def get_data(
        self,
        series_ids: list[str],
        endpoint: Literal["metadata", "observations"],
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []

        for series_id in series_ids:
            try:
                url = self.get_url(series_id=series_id, endpoint=endpoint)
                response = httpx.get(url, timeout=10.0)
                response.raise_for_status()
                results.append({
                    "series_id": series_id,
                    "data": response.json(),
                })
            except Exception as e:
                logger.error("Error fetching %s %s: %s", series_id, endpoint, e)

        return results