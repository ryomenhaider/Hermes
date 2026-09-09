import asyncio
import logging
from datetime import timedelta
from functools import partial

import aiohttp
import polars as pl

from hermes.acquisition.cache import RawCache
from hermes.connectors.world_bank.mappings import WORLD_BANK_BASE_URL
from hermes.connectors.world_bank.parser import records_to_dataframe

logger = logging.getLogger(__name__)


class World_bank:
    def __init__(self, cache: RawCache | None = None):
        self.url = WORLD_BANK_BASE_URL
        self._cache = cache or RawCache()

    async def _fetch(
        self,
        country_code: str,
        indicator_code: str,
        frequency: str | None = None,
        most_recent: int | None = None,
        per_page: int = 1000,
        page: int = 1,
        timeout: float = 30.0,
        retries: int = 3,
    ) -> pl.DataFrame:
        url = f"{self.url}/country/{country_code}/indicator/{indicator_code}"
        params = {
            "per_page": per_page,
            "page": page,
            "format": "json",
        }
        if frequency and most_recent:
            params["frequency"] = frequency
            params["mrv"] = most_recent

        r = None
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as client:
            for attempt in range(retries):
                try:
                    resp = await client.get(url=url, params=params)
                    resp.raise_for_status()
                    r = await resp.json()
                    break
                except TimeoutError:
                    if attempt == retries - 1:
                        raise
                    await asyncio.sleep(2**attempt)
                except aiohttp.ClientResponseError as e:
                    logger.error(f"HTTP error: {e.status}")
                    raise
        if len(r) < 2 or not r[1]:
            logger.info(f"No data: country={country_code}, indicator={indicator_code}")
            return pl.DataFrame(
                schema={
                    "date": pl.String,
                    "indicator_id": pl.String,
                    "indicator_name": pl.String,
                    "country": pl.String,
                    "value": pl.String,
                    "source": pl.String,
                }
            )

        _, records = r[0], r[1]

        return records_to_dataframe(records)

    async def fetch(
        self,
        country_code: str,
        indicator_code: str,
        frequency: str | None = None,
        most_recent: int | None = None,
        per_page: int = 1000,
        page: int = 1,
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False,
    ) -> pl.DataFrame:
        cache_params = {
            "country": country_code,
            "indicator": indicator_code,
            "frequency": frequency or "",
            "most_recent": most_recent or 0,
            "per_page": per_page,
        }

        return await self._cache.get_or_fetch(
            source="world_bank",
            params=cache_params,
            fetch_fn=partial(
                self._fetch,
                country_code,
                indicator_code,
                frequency,
                most_recent,
                per_page,
                page,
                timeout,
                retries,
            ),
            force=force,
            ttl=timedelta(days=7),  # WB data updates weekly
        )
