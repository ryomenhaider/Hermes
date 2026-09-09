import asyncio
import logging
import math
from datetime import UTC, datetime, timedelta
from functools import partial

import aiohttp
import polars as pl

from hermes.acquisition.cache import RawCache
from hermes.connectors.binance.mappings import BINANCE_ENDPOINTS
from hermes.connectors.binance.parser import klines_to_dataframe
from hermes.constants import BINANCE_INTERVAL_MS

logger = logging.getLogger(__name__)


class Binance:
    def __init__(self, cache: RawCache | None = None):
        self._spot_url = "https://api.binance.com"
        self._future_url = "https://fapi.binance.com"
        self._cache = cache or RawCache()
        self._ENDPOINTS = BINANCE_ENDPOINTS

    def _build_url(
        self,
        mode: str,
        endpoint: str,
        symbol: str,
        interval: str | None = None,
        limit: str | None = None,
        period: str | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
    ):
        try:
            path, required = self._ENDPOINTS[(mode, endpoint)]
        except KeyError:
            raise ValueError(f"unknown endpoint {endpoint!r} for mode {mode!r}")

        base_url = self._spot_url if mode == "spot" else self._future_url
        params = {"symbol": symbol}

        provided = {"interval": interval, "limit": limit, "period": period}
        for name in required:
            if provided[name] is None:
                raise ValueError(f"{mode}/{endpoint} requires {name!r}")
            params[name] = provided[name]

        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time

        return f"{base_url.rstrip('/')}/{path}", params

    async def _fetch(
        self,
        mode: str,
        endpoint: str,
        symbol: str,
        interval: str | None = None,
        limit: int | None = None,
        period: str | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        retries: int = 3,
        timeout: float = 30.0,
    ):
        url, params = self._build_url(
            mode=mode,
            endpoint=endpoint,
            symbol=symbol,
            interval=interval,
            limit=limit,
            period=period,
            start_time=start_time,
            end_time=end_time,
        )

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
        mode: str,
        endpoint: str,
        symbol: str,
        interval: str | None = None,
        limit: int | None = None,
        period: str | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        retries: int = 3,
        timeout: float = 30.0,
        force: bool = False,
    ):
        cached_params = {
            "symbol": symbol,
            "mode": mode,
            "endpoint": endpoint,
            "start_time": start_time,
            "end_time": end_time,
        }

        return await self._cache.get_or_fetch(
            source="binance",
            params=cached_params,
            fetch_fn=partial(
                self._fetch,
                endpoint=endpoint,
                symbol=symbol,
                interval=interval,
                limit=limit,
                period=period,
                mode=mode,
                start_time=start_time,
                end_time=end_time,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=1),
        )

    async def fetch_history(
        self,
        symbol: str,
        interval: str = "1d",
        market: str = "future",
        years: int = 2,
        max_concurrent: int = 10,
    ) -> pl.DataFrame:
        interval_ms = BINANCE_INTERVAL_MS.get(interval)
        if interval_ms is None:
            raise ValueError(f"Unsupported interval: {interval!r}")

        now_ms = int(datetime.now(UTC).timestamp() * 1000)
        start_ms = now_ms - (years * 365 * 86_400_000)
        per_request_ms = 1000 * interval_ms

        num_requests = math.ceil((now_ms - start_ms) / per_request_ms)
        semaphore = asyncio.Semaphore(max_concurrent)

        async def _fetch_window(window_start: int, window_end: int) -> list:
            async with semaphore:
                data = await self.fetch(
                    mode=market,
                    endpoint="ohlcv",
                    symbol=symbol,
                    interval=interval,
                    limit=1000,
                    start_time=window_start,
                    end_time=window_end,
                    force=True,
                )
                return data if data else []

        tasks = []
        for i in range(num_requests):
            window_start = start_ms + (i * per_request_ms)
            window_end = min(window_start + per_request_ms, now_ms)
            tasks.append(_fetch_window(window_start, window_end))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_candles = []
        for r in results:
            if isinstance(r, list):
                all_candles.extend(r)
            else:
                logger.warning(f"History fetch error: {r}")

        return klines_to_dataframe(all_candles)
