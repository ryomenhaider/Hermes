import asyncio
import logging
from datetime import timedelta
from functools import partial

import aiohttp
import polars as pl

from hermes.acquisition.cache import RawCache
from hermes.entities.companies import get_cik

logger = logging.getLogger(__name__)


class SECEDGAR:
    def __init__(self, username: str, email: str, cache: RawCache | None = None):
        self._email = email
        self._username = username
        self._cache = cache or RawCache()
        self._url = "https://data.sec.gov/api/xbrl/companyfacts"

    async def _fetch(self, symbol: str, retries: int = 3, timeout: float = 30.0):
        cik = get_cik(ticker=symbol)
        url = f"{self._url}/{cik}.json"

        headers = {"User-Agent": f"{self._username} {self._email}"}

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
                        logger.warning("404")
                        return r
                    logger.error(f"HTTP error: {e.status}")
                    raise

        return r

    async def fetch(
        self,
        symbol: str,
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False,
    ) -> pl.DataFrame | dict:
        cache_params = {
            "company": symbol,
        }

        return await self._cache.get_or_fetch(
            source="sec_edgar",
            params=cache_params,
            fetch_fn=partial(
                self._fetch,
                symbol=symbol,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=7),
        )
