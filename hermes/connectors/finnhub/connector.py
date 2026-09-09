import asyncio
import logging
from datetime import UTC, datetime, timedelta
from functools import partial

import aiohttp
import polars as pl

from hermes.acquisition.cache import RawCache
from hermes.connectors.finnhub.mappings import BASE_URL, ENDPOINTS, FinnhubEndpoint
from hermes.connectors.finnhub.parser import candles_to_dataframe
from hermes.constants import FINNHUB_MAX_DAYS

logger = logging.getLogger(__name__)


class FINNHUB:
    BASE_URL = BASE_URL

    ENDPOINTS = ENDPOINTS

    def __init__(
        self,
        api: str,
        cache: RawCache | None = None,
    ):
        self._api = api
        self._cache = cache or RawCache()
        self._url = self.BASE_URL

    def build_url(
        self,
        endpoint: FinnhubEndpoint,
    ) -> str:
        try:
            path = self.ENDPOINTS[endpoint]
        except KeyError:
            raise ValueError(f"Unsupported endpoint: {endpoint}")

        return f"{self._url}/{path}"

    async def _fetch(
        self,
        endpoint: str,
        symbol: str,
        resolution: str | None = None,
        timeout: float = 30.0,
        retries: int = 3,
        _from: int | None = None,
        _to: int | None = None,
    ):
        params = {"token": self._api, "symbol": symbol}

        _url = self.build_url(endpoint=endpoint)

        if endpoint == "candles":
            if None in (resolution, _from, _to):
                raise ValueError("this endpoint requires resolution, _from and _to arguments")
            params["resolution"] = resolution
            params["from"] = _from
            params["to"] = _to
        elif endpoint == "metric":
            params["metric"] = "all"
        elif endpoint == "insider":
            if None in (_from, _to):
                raise ValueError("this endpoint requires _from and _to arguments")
            params["from"] = _from
            params["to"] = _to
        elif endpoint == "news":
            if None in (_from, _to):
                raise ValueError("this endpoint requires _from and _to arguments")
            params["from"] = _from
            params["to"] = _to

        r = None

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as client:
            for attempt in range(retries):
                try:
                    resp = await client.get(url=_url, params=params)
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
                    if e.status == 403:
                        logger.error("error 403")
                        continue
                    logger.error(f"HTTP error: {e.status}")
                    raise
        return r

    async def fetch(
        self,
        endpoint: str,
        symbol: str,
        resolution: str | None = None,
        _from: int | None = None,
        _to: int | None = None,
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False,
    ):
        cached_params = {
            "endpoint": endpoint,
            "symbol": symbol,
            "resolution": resolution,
            "_to": _to,
            "_from": _from,
        }

        return await self._cache.get_or_fetch(
            source="finnhub",
            params=cached_params,
            fetch_fn=partial(
                self._fetch,
                endpoint=endpoint,
                symbol=symbol,
                resolution=resolution,
                _from=_from,
                _to=_to,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=7),
        )

    async def fetch_candles_history(
        self,
        symbol: str,
        resolution: str = "D",
        years: int = 2,
    ) -> pl.DataFrame:
        max_days = FINNHUB_MAX_DAYS.get(resolution, 365)
        now = int(datetime.now(UTC).timestamp())
        start = now - (years * 365 * 86_400)
        chunk_seconds = max_days * 86_400

        all_candles = []
        chunk_start = start

        while chunk_start < now:
            chunk_end = min(chunk_start + chunk_seconds, now)
            data = await self.fetch(
                endpoint="candles",
                symbol=symbol,
                resolution=resolution,
                _from=chunk_start,
                _to=chunk_end,
                force=True,
            )
            if data and data.get("s") == "ok":
                candles = list(
                    zip(
                        data["t"],
                        data["o"],
                        data["h"],
                        data["l"],
                        data["c"],
                        data["v"],
                    )
                )
                all_candles.extend(candles)
            chunk_start = chunk_end + 1

        return candles_to_dataframe(all_candles)
