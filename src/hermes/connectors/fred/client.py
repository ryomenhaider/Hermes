import httpx
import logging
from typing import Literal

from src.hermes.config import FRED_API
from src.hermes.connectors.fred.indicators import FRED_INDICATORS

logger = logging.getLogger(__name__)

class FredClient:

    def __init__(self):
        self._api = FRED_API

    def get_url(
        self,
        series_id: str,
        endpoint: Literal["metadata", "observations"] = "metadata"
    ) -> str:

        valid_series_ids = {
            item["series_id"]
            for item in FRED_INDICATORS
        }

        if series_id not in valid_series_ids:
            raise ValueError(f"{series_id} is not available")

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


    def get_data(self, endpoint: Literal['metadata', 'observations']):

        results = []

        for item in FRED_INDICATORS:
            try:
                series_id = item['series_id']
                url = self.get_url(
                    series_id=series_id,
                    endpoint=endpoint
                )

                response = httpx.get(url, timeout=10.0)
                response.raise_for_status()

                results.append(
                    {
                        'series_id': series_id,
                        'data': response.json()
                    }
                )

            except Exception as e:
                logger.error(f'Error fetching {series_id} {endpoint}: {e}')

        return results
    
if __name__ == '__main__':
    fred_c = FredClient()

    print(fred_c.get_url('GDP', 'observations'))