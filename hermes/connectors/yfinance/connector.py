import logging
from datetime import timedelta
from functools import partial

import polars as pl

try:
    import yfinance as yf
except ImportError:
    pass

from hermes.acquisition.cache import RawCache
from hermes.connectors.base import BaseConnector
from hermes.connectors.yfinance.mappings import YfinanceEndpoint, YFINANCE_INTERVAL_MAP
from hermes.validation import NotNull

logger = logging.getLogger(__name__)


class Yfinance(BaseConnector):
    canonical_schema = "market.observation"

    def __init__(
        self,
        cache: RawCache | None = None,
    ):
        super().__init__(cache)

    def _fetch(
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

    def fetch(
        self,
        endpoint: YfinanceEndpoint,
        symbol: str,
        force: bool = False,
    ):
        cached_params = {
            "endpoint": endpoint,
            "symbol": symbol,
        }

        payload = self._cache.get_or_fetch(
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
        if payload is None:
            return payload
        return self._dataset(payload, f"yfinance:{symbol}:{endpoint}", source="yfinance", params=cached_params)

    def fetch_history(
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

        df = _sync_history()

        df = history_to_dataframe(df)
        self._validate(df, [NotNull("timestamp_ms"), NotNull("close")], "yfinance")
        return df
