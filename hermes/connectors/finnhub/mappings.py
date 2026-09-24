from typing import Literal

FinnhubEndpoint = Literal[
    "candles",
    "quote",
    "profile",
    "metric",
    "peers",
    "earnings",
    "insider",
    "eps",
    "ebitda",
    "revenue",
    "news",
    "symbol",
]
FinnhubEndpoints = [
    "candles",
    "quote",
    "profile",
    "metric",
    "peers",
    "earnings",
    "insider",
    "eps",
    "ebitda",
    "revenue",
    "news",
    "symbol",
]

BASE_URL = "https://finnhub.io/api/v1"

ENDPOINTS = {
    "candles": "stock/candle",
    "quote": "quote",
    "profile": "stock/profile2",
    "metric": "stock/metric",
    "peers": "stock/peers",
    "earnings": "stock/earnings",
    "insider": "stock/insider-sentiment",
    "eps": "stock/eps-estimate",
    "ebitda": "stock/ebitda-estimate",
    "revenue": "stock/revenue-estimate",
    "news": "company-news",
    "symbol": "stock/symbol",
}

FINNHUB_MAX_DAYS = {
    "1": 7,
    "5": 7,
    "15": 30,
    "30": 30,
    "60": 30,
    "D": 365,
    "W": 365,
    "M": 365,
}

__all__ = ["FinnhubEndpoint", "FinnhubEndpoints", "BASE_URL", "ENDPOINTS", "FINNHUB_MAX_DAYS"]
