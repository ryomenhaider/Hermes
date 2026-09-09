import asyncio
import logging
from datetime import timedelta
from functools import partial

import pandas as pd
import polars as pl
import yfinance as yf

from hermes.acquisition.cache import RawCache
from hermes.connectors.yfinance.mappings import YfinanceEndpoint
from hermes.connectors.yfinance.parser import history_to_dataframe
from hermes.constants import YFINANCE_INTERVAL_MAP

logger = logging.getLogger(__name__)


class Yfinance:
    def __init__(
        self,
        cache: RawCache | None = None,
    ):
        self._cache = cache or RawCache()

    async def _fetch(
        self,
        endpoint: YfinanceEndpoint,
        symbol: str,
    ):
        ticker = yf.Ticker(symbol)

        if endpoint == "quote":
            return ticker.info
        elif endpoint == "eps_estimate":
            df = ticker.earnings_estimate
            return df.to_dict() if df is not None and not df.empty else None
        elif endpoint == "revenue_estimate":
            df = ticker.revenue_estimate
            return df.to_dict() if df is not None and not df.empty else None
        elif endpoint == "earnings_history":
            df = ticker.earnings_history
            return df.to_dict() if df is not None and not df.empty else None
        else:
            raise ValueError(f"Unsupported endpoint: {endpoint}")

    async def fetch(
        self,
        endpoint: YfinanceEndpoint,
        symbol: str,
        force: bool = False,
    ):
        cached_params = {
            "endpoint": endpoint,
            "symbol": symbol,
        }

        return await self._cache.get_or_fetch(
            source="yfinance",
            params=cached_params,
            fetch_fn=partial(
                self._fetch,
                endpoint=endpoint,
                symbol=symbol,
            ),
            force=force,
            ttl=timedelta(days=1),
        )

    async def fetch_history(
        self,
        symbol: str,
        interval: str = "1d",
        years: int = 2,
    ) -> pl.DataFrame:
        yf_interval = YFINANCE_INTERVAL_MAP.get(interval)
        if yf_interval is None:
            raise ValueError(
                f"Interval {interval!r} not supported for stocks. Supported: {list(YFINANCE_INTERVAL_MAP.keys())}"
            )

        def _sync_history():
            ticker = yf.Ticker(symbol)
            return ticker.history(period=f"{years}y", interval=yf_interval)

        df = await asyncio.get_event_loop().run_in_executor(None, _sync_history)

        return history_to_dataframe(df)
