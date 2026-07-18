from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

STD_FEATURES: dict[str, dict[str, Any]] = {
    "gdp_growth_yoy": {"category": "economic", "description": "GDP year-over-year growth rate", "unit": "%"},
    "gdp_growth_qoq": {"category": "economic", "description": "GDP quarter-over-quarter growth rate", "unit": "%"},
    "industrial_production_yoy": {"category": "economic", "description": "Industrial production YoY", "unit": "%"},
    "inflation_cpi_yoy": {"category": "economic", "description": "CPI inflation YoY", "unit": "%"},
    "inflation_volatility_12m": {"category": "economic", "description": "12-month rolling std of CPI YoY", "unit": "%"},
    "ppi_yoy": {"category": "economic", "description": "Producer price index YoY", "unit": "%"},
    "unemployment_rate": {"category": "economic", "description": "Unemployment rate", "unit": "%"},
    "youth_unemployment": {"category": "economic", "description": "Youth unemployment rate (15-24)", "unit": "%"},
    "labor_force_participation": {"category": "economic", "description": "Labor force participation rate", "unit": "%"},
    "gdp_per_capita_ppp": {"category": "economic", "description": "GDP per capita PPP", "unit": "USD"},
    "gdp_current_usd": {"category": "economic", "description": "GDP current USD", "unit": "USD"},
    "exports": {"category": "trade", "description": "Exports of goods and services", "unit": "USD"},
    "imports": {"category": "trade", "description": "Imports of goods and services", "unit": "USD"},
    "trade_balance": {"category": "trade", "description": "Exports - Imports", "unit": "USD"},
    "current_account_gdp_ratio": {"category": "external", "description": "Current account balance % of GDP", "unit": "%"},
    "fx_reserves_months_import": {"category": "external", "description": "FX reserves in months of imports", "unit": "months"},
    "external_debt_gdp_ratio": {"category": "external", "description": "External debt % of GDP", "unit": "%"},
    "fiscal_deficit_gdp": {"category": "fiscal", "description": "Fiscal deficit % of GDP", "unit": "%"},
    "government_debt_gdp": {"category": "fiscal", "description": "Government debt % of GDP", "unit": "%"},
    "credit_spread_bps": {"category": "financial", "description": "Sovereign credit spread in bps", "unit": "bps"},
    "yield_curve_10y_2y": {"category": "financial", "description": "10Y-2Y yield curve spread", "unit": "%"},
    "banking_sector_health": {"category": "financial", "description": "Banking sector health indicator (0-100)", "unit": "score"},
    "regime_classification": {"category": "governance", "description": "Regime type (democracy/hybrid/autocracy)", "unit": "category"},
    "goldstein_score_violence": {"category": "security", "description": "Goldstein violence score (0-1)", "unit": "score"},
    "civil_unrest_risk": {"category": "security", "description": "Probability of civil unrest (0-1)", "unit": "probability"},
    "news_sentiment_7d": {"category": "sentiment", "description": "7-day average news sentiment (-1 to 1)", "unit": "score"},
    "governance_effectiveness": {"category": "governance", "description": "World Bank Governance Effectiveness", "unit": "score"},
    "rule_of_law": {"category": "governance", "description": "World Bank Rule of Law", "unit": "score"},
    "corruption_control": {"category": "governance", "description": "World Bank Corruption Control", "unit": "score"},
    "sovereign_rating": {"category": "sovereign", "description": "S&P/Moody's/Fitch sovereign rating", "unit": "rating"},
    "rating_outlook": {"category": "sovereign", "description": "Sovereign rating outlook", "unit": "outlook"},
}


def list_available() -> list[dict[str, Any]]:
    return [
        {"name": k, **v}
        for k, v in sorted(STD_FEATURES.items())
    ]


def freshness(
    last_updated: dict[str, str | None] | None = None,
) -> dict[str, str]:
    if last_updated is None:
        return {k: "unknown" for k in STD_FEATURES}
    return {
        k: last_updated.get(k, "unknown") or "unknown"
        for k in STD_FEATURES
    }
