import asyncio
import logging
from datetime import timedelta
from functools import partial

import aiohttp
import polars as pl

from hermes.acquisition.cache import RawCache
from hermes.connectors.imf.mappings import IMF_BASE_URL
from hermes.connectors.imf.parser import empty_dataframe, parse_sdmx_json

logger = logging.getLogger(__name__)


class IMF:
    def __init__(self, cache: RawCache | None = None):
        self._cache = cache or RawCache()
        self.url: str = IMF_BASE_URL

    async def _fetch(
        self,
        country: str,
        agency: str,
        dataflow_id: str,
        key: str,
        version: str = "~",
        timeout: float = 30.0,
        retries: int = 3,
    ) -> pl.DataFrame:
        url = f"{self.url}{agency}/{dataflow_id}/{version}/{country}.{key}"
        headers = {"Accept": "application/json"}

        empty = empty_dataframe()

        r = None
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as client:
            for attempt in range(retries):
                try:
                    resp = await client.get(url=url, headers=headers)
                    resp.raise_for_status()
                    r = await resp.json()
                    break
                except TimeoutError:
                    if attempt == retries - 1:
                        raise
                    await asyncio.sleep(2**attempt)
                except aiohttp.ClientResponseError as e:
                    if e.status == 404:
                        logger.warning(f"404: country={country}, dataflow={dataflow_id}, key={key}")
                        return empty
                    logger.error(f"HTTP error: {e.status}")
                    raise
        return parse_sdmx_json(r["data"], country=country, key=key)

    async def normalize(self, data):
        return data

    async def fetch(
        self,
        country: str,
        agency: str,
        dataflow_id: str,
        key: str,
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False,
    ) -> pl.DataFrame:
        cache_params = {
            "country": country,
            "key": key,
            "agency": agency,
            "dataflow_id": dataflow_id,
        }

        return await self._cache.get_or_fetch(
            source="imf",
            params=cache_params,
            fetch_fn=partial(
                self._fetch,
                country=country,
                agency=agency,
                dataflow_id=dataflow_id,
                key=key,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=7),
        )
