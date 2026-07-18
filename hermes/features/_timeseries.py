"""Time series retrieval for forecasting and anomaly detection."""

from typing import Any

import pandas as pd


def get_timeseries(
    connectors: dict[str, Any],
    country: str,
    indicator: str,
    start: str = "",
    end: str = "",
) -> list[dict]:
    source = _detect_source(indicator)
    connector = connectors.get(source)
    if connector is None:
        return []

    try:
        df = connector.fetch(indicator=indicator, country=country)
    except Exception:
        return []

    if df.empty:
        return []

    df = df[df["country"] == country.upper()].copy()
    if start:
        df = df[df["date"] >= pd.Timestamp(start)]
    if end:
        df = df[df["date"] <= pd.Timestamp(end)]

    return df.sort_values("date")[["date", "value"]].to_dict(orient="records")


def get_raw_indicator(
    connectors: dict[str, Any],
    country: str,
    indicator: str,
    source: str,
    start: str = "",
    end: str = "",
) -> list[dict]:
    connector = connectors.get(source)
    if connector is None:
        return []

    try:
        df = connector.fetch(indicator=indicator, country=country)
    except Exception:
        return []

    if df.empty:
        return []

    df = df[df["country"] == country.upper()].copy()
    if start:
        df = df[df["date"] >= pd.Timestamp(start)]
    if end:
        df = df[df["date"] <= pd.Timestamp(end)]

    return df.sort_values("date")[["date", "value"]].to_dict(orient="records")


_INDICATOR_SOURCE: dict[str, str] = {
    "gdp_growth_yoy": "fred",
    "gdp_growth_qoq": "fred",
    "industrial_production_yoy": "fred",
    "inflation_cpi_yoy": "fred",
    "inflation_volatility_12m": "fred",
    "ppi_yoy": "fred",
    "unemployment_rate": "fred",
    "youth_unemployment": "world_bank",
    "labor_force_participation": "fred",
    "current_account_gdp_ratio": "imf",
    "fx_reserves_months_import": "imf",
    "external_debt_gdp_ratio": "world_bank",
    "fiscal_deficit_gdp": "imf",
    "government_debt_gdp": "imf",
    "credit_spread_bps": "fred",
    "yield_curve_10y_2y": "fred",
    "banking_sector_health": "bis",
    "gdp_per_capita_ppp": "world_bank",
}


def _detect_source(indicator: str) -> str:
    return _INDICATOR_SOURCE.get(indicator, "fred")
