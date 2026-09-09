import asyncio
import logging
from datetime import timedelta
from functools import partial

import aiohttp
import polars as pl

from hermes.acquisition.cache import RawCache
from hermes.connectors.fred.parser import observations_to_dataframe

logger = logging.getLogger(__name__)


class FRED:
    def __init__(self, api: str, cache: RawCache | None = None):
        self._cache = cache or RawCache()
        self._url = "https://api.stlouisfed.org/fred/series/observations"
        self._api = api

    async def _fetch(self, series_id: str, timeout: float = 30.0, retries: int = 3) -> pl.DataFrame:
        params = {"series_id": series_id, "api_key": self._api, "file_type": "json"}

        r = None
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as client:
            for attempt in range(retries):
                try:
                    resp = await client.get(url=self._url, params=params)
                    resp.raise_for_status()
                    r = await resp.json()
                    break
                except TimeoutError:
                    if attempt == retries - 1:
                        raise
                    await asyncio.sleep(2**attempt)
                except aiohttp.ClientResponseError as e:
                    if e.status == 404:
                        logger.warning("404")
                        return r
                    logger.error(f"HTTP error: {e.status}")
                    raise

        return observations_to_dataframe(r, series_id)

    async def fetch(self, series_id: str, timeout: float = 30.0, retries: int = 3, force: bool = False) -> pl.DataFrame:
        cached_params = {"series_id": series_id}

        return await self._cache.get_or_fetch(
            source="fred",
            params=cached_params,
            fetch_fn=partial(
                self._fetch,
                series_id=series_id,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=30),
        )
