import logging
import math
from datetime import UTC, datetime, timedelta
from functools import partial

import polars as pl

from hermes.acquisition.cache import RawCache
from hermes.connectors.base import BaseConnector
from hermes.connectors.binance.mappings import BINANCE_ENDPOINTS, BINANCE_INTERVAL_MS
from hermes.connectors.binance.parser import klines_to_dataframe
from hermes.core.errors import AcquisitionError
from hermes.validation import NotNull

logger = logging.getLogger(__name__)


class Binance(BaseConnector):
    canonical_schema = "market.observation"
    def __init__(self, cache: RawCache | None = None):
        super().__init__(cache, retry_auth=True)
        self._spot_url = "https://api.binance.com"
        self._future_url = "https://fapi.binance.com"
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

    def _fetch(
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

        try:
            return self._get_json(url, params=params, timeout=timeout, retries=retries)
        except AcquisitionError as e:
            if self._not_found(e):
                logger.warning("404")
                return None
            logger.error("HTTP error: %s", e)
            raise

    def fetch(
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

        payload = self._cache.get_or_fetch(
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
        if payload is None:
            return payload
        return self._dataset(payload, f"binance:{symbol}:{mode}:{endpoint}", source="binance", params=cached_params)

    def fetch_history(
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

        all_candles = []
        for i in range(num_requests):
            window_start = start_ms + (i * per_request_ms)
            window_end = min(window_start + per_request_ms, now_ms)
            try:
                data = self.fetch(
                    mode=market,
                    endpoint="ohlcv",
                    symbol=symbol,
                    interval=interval,
                    limit=1000,
                    start_time=window_start,
                    end_time=window_end,
                    force=True,
                )
            except Exception as e:
                logger.warning(f"History fetch error: {e}")
                continue
            if data:
                all_candles.extend(data)

        df = klines_to_dataframe(all_candles)
        self._validate(df, [NotNull("open_time"), NotNull("close")], "binance")
        return df
