from typing import Literal

YfinanceEndpoint = Literal[
    "eps_estimate",
    "revenue_estimate",
    "earnings_history",
]

YfinanceEndpoints = [
    "eps_estimate",
    "revenue_estimate",
    "earnings_history",
]

YFINANCE_INTERVAL_MAP = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "1d": "1d",
    "1w": "1wk",
    "1M": "1mo",
}

__all__ = ["YfinanceEndpoint", "YfinanceEndpoints", "YFINANCE_INTERVAL_MAP"]
