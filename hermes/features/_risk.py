from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

import numpy as np
import pandas as pd

from hermes.features._composite import (
    categorize_regime,
    classify_trend,
    goldstein_to_violence,
    max_drawdown,
    rolling_volatility,
    yoy_growth,
    qoq_growth,
)

logger = logging.getLogger(__name__)

_STD_RISK_FEATURES = [
    "gdp_growth_yoy",
    "gdp_growth_qoq",
    "industrial_production_yoy",
    "inflation_cpi_yoy",
    "inflation_volatility_12m",
    "ppi_yoy",
    "unemployment_rate",
    "youth_unemployment",
    "labor_force_participation",
    "current_account_gdp_ratio",
    "fx_reserves_months_import",
    "external_debt_gdp_ratio",
    "fiscal_deficit_gdp",
    "government_debt_gdp",
    "credit_spread_bps",
    "yield_curve_10y_2y",
    "banking_sector_health",
    "gdp_per_capita_ppp",
    "gdp_current_usd",
    "exports",
    "imports",
    "trade_balance",
    "gdp_growth_forecast",
    "inflation_forecast",
    "unemployment_forecast",
    "trend_classification",
    "regime_classification",
    "goldstein_score_violence",
    "civil_unrest_risk",
    "news_sentiment_7d",
    "governance_effectiveness",
    "rule_of_law",
    "corruption_control",
    "sovereign_rating",
    "rating_outlook",
]


def get_country_risk_features(
    country: str,
    date: str | None = None,
    connectors: dict[str, Any] | None = None,
    cache: Any = None,
    features: list[str] | None = None,
) -> dict[str, Any]:
    date_obj = pd.Timestamp(date) if date else pd.Timestamp.now()
    country = country.upper()
    connectors = connectors or {}

    requested = features or _STD_RISK_FEATURES
    result: dict[str, Any] = {}

    fred = connectors.get("fred")
    wb = connectors.get("world_bank")
    imf = connectors.get("imf")
    bis = connectors.get("bis")

    raw_econ: dict[str, pd.DataFrame] = {}
    for name, conn in [("fred", fred), ("world_bank", wb), ("imf", imf), ("bis", bis)]:
        if conn is not None:
            try:
                series_df = conn.fetch(country=country)
                if not series_df.empty:
                    raw_econ[name] = series_df
            except Exception:
                logger.debug("No data from %s for %s", name, country)

    _populate_economic(result, raw_econ, country, date_obj, requested)
    _populate_financial(result, raw_econ, country, date_obj, requested)
    _populate_sovereign(result, raw_econ, country, date_obj, requested)

    result["country"] = country
    result["as_of_date"] = date_obj.isoformat()
    return result


def _fetch_one(connector: Any, indicator: str, country: str) -> pd.Series:
    try:
        df = connector.fetch(indicator=indicator, country=country)
        if df.empty:
            return pd.Series(dtype=float)
        country_df = df[df["country"] == country.upper()]
        if country_df.empty:
            return pd.Series(dtype=float)
        return country_df.set_index("date")["value"]
    except Exception:
        return pd.Series(dtype=float)


def _populate_economic(
    result: dict, raw: dict, country: str, date: pd.Timestamp, requested: list[str]
) -> None:
    if "gdp_growth_yoy" in requested:
        s = pd.Series(dtype=float)
        if "fred" in raw and "GDPC1" in raw["fred"]["indicator"].values:
            gdp = raw["fred"].loc[raw["fred"]["indicator"] == "GDPC1"].set_index("date")["value"]
            if len(gdp) >= 5:
                s = yoy_growth(gdp)
        result["gdp_growth_yoy"] = _at_date(s, date)

    if "gdp_growth_qoq" in requested:
        s = pd.Series(dtype=float)
        if "fred" in raw and "GDPC1" in raw["fred"]["indicator"].values:
            gdp = raw["fred"].loc[raw["fred"]["indicator"] == "GDPC1"].set_index("date")["value"]
            if len(gdp) >= 2:
                s = qoq_growth(gdp)
        result["gdp_growth_qoq"] = _at_date(s, date)

    if "industrial_production_yoy" in requested:
        s = _fetch_one(raw.get("fred"), "INDPRO", country)
        if len(s) >= 5:
            s = yoy_growth(s)
        result["industrial_production_yoy"] = _latest(s)

    if "inflation_cpi_yoy" in requested:
        s = _fetch_one(raw.get("fred"), "CPIAUCSL", country)
        if len(s) >= 5:
            s = yoy_growth(s)
        result["inflation_cpi_yoy"] = _latest(s)

    if "inflation_volatility_12m" in requested:
        s = _fetch_one(raw.get("fred"), "CPIAUCSL", country)
        if len(s) >= 5:
            yoy = yoy_growth(s)
            result["inflation_volatility_12m"] = rolling_volatility(yoy, window=12)
        else:
            result["inflation_volatility_12m"] = 0.0

    if "ppi_yoy" in requested:
        s = _fetch_one(raw.get("fred"), "PPIACO", country)
        if len(s) >= 5:
            s = yoy_growth(s)
        result["ppi_yoy"] = _latest(s)

    if "unemployment_rate" in requested:
        s = _fetch_one(raw.get("fred"), "UNRATE", country)
        result["unemployment_rate"] = _latest(s)

    if "labor_force_participation" in requested:
        s = _fetch_one(raw.get("fred"), "CIVPART", country)
        result["labor_force_participation"] = _latest(s)

    if "gdp_per_capita_ppp" in requested:
        s = _fetch_one(raw.get("world_bank"), "NY.GDP.PCAP.PP.KD", country)
        result["gdp_per_capita_ppp"] = _latest(s)

    if "gdp_current_usd" in requested:
        s = _fetch_one(raw.get("world_bank"), "NY.GDP.MKTP.CD", country)
        result["gdp_current_usd"] = _latest(s)

    if "exports" in requested:
        s = _fetch_one(raw.get("world_bank"), "NE.EXP.GNFS.CD", country)
        result["exports"] = _latest(s)

    if "imports" in requested:
        s = _fetch_one(raw.get("world_bank"), "NE.IMP.GNFS.CD", country)
        result["imports"] = _latest(s)

    if "trade_balance" in requested:
        ex = _latest(_fetch_one(raw.get("world_bank"), "NE.EXP.GNFS.CD", country))
        im = _latest(_fetch_one(raw.get("world_bank"), "NE.IMP.GNFS.CD", country))
        result["trade_balance"] = (ex - im) if (ex is not None and im is not None) else None

    if "youth_unemployment" in requested:
        s = _fetch_one(raw.get("world_bank"), "SL.UEM.1524.ZS", country)
        result["youth_unemployment"] = _latest(s)

    if "current_account_gdp_ratio" in requested:
        s = _fetch_one(raw.get("imf"), "BCA_BP6_USD", country)
        gdp = _fetch_one(raw.get("world_bank"), "NY.GDP.MKTP.CD", country)
        ca_val = _latest(s) or _latest(_fetch_one(raw.get("fred"), "NETFI", country))
        gdp_val = _latest(gdp)
        if ca_val and gdp_val:
            result["current_account_gdp_ratio"] = (ca_val / gdp_val) * 100
        else:
            result["current_account_gdp_ratio"] = None

    if "fx_reserves_months_import" in requested:
        reserves = _latest(_fetch_one(raw.get("imf"), "RES_USD", country))
        imports_val = _latest(_fetch_one(raw.get("world_bank"), "NE.IMP.GNFS.CD", country))
        if reserves and imports_val:
            result["fx_reserves_months_import"] = reserves / (imports_val / 12)
        else:
            result["fx_reserves_months_import"] = None

    if "external_debt_gdp_ratio" in requested:
        debt = _latest(_fetch_one(raw.get("world_bank"), "DT.DOD.DECT.CD", country))
        gdp = _latest(_fetch_one(raw.get("world_bank"), "NY.GDP.MKTP.CD", country))
        result["external_debt_gdp_ratio"] = ((debt / gdp) * 100) if debt and gdp else None


def _populate_financial(
    result: dict, raw: dict, country: str, date: pd.Timestamp, requested: list[str]
) -> None:
    if "fiscal_deficit_gdp" in requested:
        s = _fetch_one(raw.get("imf"), "GGB_G01", country)
        result["fiscal_deficit_gdp"] = _latest(s)

    if "government_debt_gdp" in requested:
        s = _fetch_one(raw.get("imf"), "GGXWDG_NGDP", country)
        if s.empty:
            s = _fetch_one(raw.get("fred"), "GFDEGDQ188S", country)
        result["government_debt_gdp"] = _latest(s)

    if "credit_spread_bps" in requested:
        result["credit_spread_bps"] = None

    if "yield_curve_10y_2y" in requested:
        if country == "USA":
            t10 = _fetch_one(raw.get("fred"), "DGS10", country)
            t2 = _fetch_one(raw.get("fred"), "DGS2", country)
            if not t10.empty and not t2.empty:
                spread = (t10 - t2).dropna()
                result["yield_curve_10y_2y"] = _latest(spread)
        else:
            result["yield_curve_10y_2y"] = None

    if "banking_sector_health" in requested:
        s = _fetch_one(raw.get("bis"), "TOTAL_CREDIT", country)
        if not s.empty and len(s) >= 5:
            yoy = yoy_growth(s)
            val = _latest(yoy)
            if val is not None:
                result["banking_sector_health"] = max(0.0, 100.0 - abs(val))
        result["banking_sector_health"] = result.get("banking_sector_health", 50.0)


def _populate_sovereign(
    result: dict, raw: dict, country: str, date: pd.Timestamp, requested: list[str]
) -> None:
    if "trend_classification" in requested:
        recent = result.get("inflation_cpi_yoy")
        prior = None
        result["trend_classification"] = classify_trend(recent, prior)

    if "regime_classification" in requested:
        s = _fetch_one(raw.get("world_bank"), "PV.EST", country)
        dem_score = _latest(s)
        result["regime_classification"] = categorize_regime(dem_score)

    if "goldstein_score_violence" in requested:
        result["goldstein_score_violence"] = 0.5

    if "civil_unrest_risk" in requested:
        result["civil_unrest_risk"] = 0.5

    if "news_sentiment_7d" in requested:
        result["news_sentiment_7d"] = 0.0

    if "governance_effectiveness" in requested:
        s = _fetch_one(raw.get("world_bank"), "GE.EST", country)
        result["governance_effectiveness"] = _latest(s)

    if "rule_of_law" in requested:
        s = _fetch_one(raw.get("world_bank"), "RL.EST", country)
        result["rule_of_law"] = _latest(s)

    if "corruption_control" in requested:
        s = _fetch_one(raw.get("world_bank"), "CC.EST", country)
        result["corruption_control"] = _latest(s)

    if "sovereign_rating" in requested:
        result["sovereign_rating"] = None

    if "rating_outlook" in requested:
        result["rating_outlook"] = None

    if "gdp_growth_forecast" in requested:
        result["gdp_growth_forecast"] = result.get("gdp_growth_yoy")

    if "inflation_forecast" in requested:
        result["inflation_forecast"] = result.get("inflation_cpi_yoy")

    if "unemployment_forecast" in requested:
        result["unemployment_forecast"] = result.get("unemployment_rate")


def _at_date(s: pd.Series, date: pd.Timestamp) -> float | None:
    dates = s.dropna()
    if dates.empty:
        return None
    target = dates.index[dates.index.to_series().sub(date).abs().argmin()]
    return float(dates.loc[target]) if pd.notna(dates.loc[target]) else None


def _latest(s: pd.Series) -> float | None:
    s = s.dropna()
    return float(s.iloc[-1]) if not s.empty else None
