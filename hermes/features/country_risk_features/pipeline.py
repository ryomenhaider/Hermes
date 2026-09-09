import asyncio
import logging
from collections.abc import Callable
from datetime import datetime
from typing import Any

import polars as pl

from hermes.entities.countries import check_iso3
from hermes.features.country_risk_features.economic import economic_features
from hermes.features.country_risk_features.environmental import enviromental_features
from hermes.features.country_risk_features.geopolitical import geopolitical_features
from hermes.features.country_risk_features.security import security_features
from hermes.features.country_risk_features.social import social_features

logger = logging.getLogger(__name__)


async def _await_group(fns: dict[str, Callable[..., Any]]) -> dict[str, Any]:
    async def _safe_call(fn):
        try:
            return await fn()
        except Exception as e:
            logger.warning(f"Feature failed: {e}")
            return None

    values = await asyncio.gather(*(_safe_call(f) for f in fns.values()))
    return dict(zip(fns.keys(), values))


def _normalize_key(df: pl.DataFrame, key_col: str) -> pl.DataFrame:
    """Force the panel key to a consistent Date on Jan 1 for year-like columns."""
    dtype = df.schema[key_col]
    if dtype == pl.Date:
        return df
    if dtype == pl.Datetime:
        return df.with_columns(pl.col(key_col).cast(pl.Date).alias(key_col))
    return df.with_columns(pl.col(key_col).cast(pl.Utf8).str.to_date("%Y").alias(key_col))


class pipeline:
    def __init__(self, os_api: str):
        self.eco = economic_features()
        self.env = enviromental_features()
        self.geo = geopolitical_features(os_api=os_api)
        self.sec = security_features()
        self.soc = social_features()
        self.os_api = os_api

    async def get_country_risk_features(self, country):
        check_iso3(code=country)
        economic = await _await_group(
            {
                "gdp_growth_yoy": lambda: self.eco.gdp_growth_yoy(country_code=country, mode="F"),
                "gdp_growth_qoq": lambda: self.eco.gdp_growth_qoq(country_code=country, mode="F"),
                "industrial_production_yoy": lambda: self.eco.industrial_production_yoy(
                    country_code=country, mode="F"
                ),  # float, percent
                "inflation_cpi_yoy": lambda: self.eco.inflation_cpi_yoy(
                    country_code=country, mode="F"
                ),  # float, percent
                "inflation_volatility_12m": lambda: self.eco.inflation_volatility_12m(
                    country_code=country, mode="F"
                ),  # float, rolling std
                "ppi_yoy": lambda: self.eco.ppi_yoy(country_code=country, mode="F"),  # float, percent
                "unemployment_rate": lambda: self.eco.unemployment_rate(
                    country_code=country, mode="F"
                ),  # float, percent
                "youth_unemployment": lambda: self.eco.youth_unemployment(
                    country_code=country, mode="F"
                ),  # float, percent
                "labor_force_participation": lambda: self.eco.labor_force_participation(
                    country_code=country, mode="F"
                ),  # float, percent
                "current_account_gdp_ratio": lambda: self.eco.current_account_gdp_ratio(
                    country_code=country, mode="F"
                ),  # float, percent of GDP
                "fx_reserves_months_import": lambda: self.eco.fx_reserves_months_import(
                    country_code=country, mode="F"
                ),  # float, months
                "external_debt_gdp_ratio": lambda: self.eco.external_debt_gdp_ratio(
                    country_code=country, mode="F"
                ),  # float, percent
                "fiscal_deficit_gdp": lambda: self.eco.fiscal_deficit_gdp(
                    country_code=country, mode="F"
                ),  # float, percent
                "government_debt_gdp": lambda: self.eco.government_debt_gdp(
                    country_code=country, mode="F"
                ),  # float, percent
                "reer_misalignment": lambda: self.eco.reer_misalignment(
                    country_code=country, mode="F"
                ),  # int, basis points
                "inflation_yoy": lambda: self.eco.inflation_yoy(
                    country_code=country, mode="F"
                ),  # float, percentage points
                "banking_sector_health": lambda: self.eco.banking_sector_health(
                    country_code=country, mode="F"
                ),  # float, 0-1 score
                "gdp_per_capita_ppp": lambda: self.eco.gdp_per_capita_ppp(country_code=country, mode="F"),  # int, USD
            }
        )
        geopolitical = await _await_group(
            {
                "conflict_event_count_30d": lambda: self.geo.conflict_event_count_30d(
                    country_code=country, mode="F"
                ),  # int
                "conflict_event_count_90d": lambda: self.geo.conflict_event_count_90d(
                    country_code=country, mode="F"
                ),  # int
                "conflict_trend": lambda: self.geo.conflict_trend(
                    country_code=country, mode="F"
                ),  # string: escalating/stable/de-escalating
                "goldstein_scale_avg_30d": lambda: self.geo.goldstein_scale_avg_30d(
                    country_code=country, mode="F"
                ),  # float, -10 to +10
                "goldstein_scale_trend": lambda: self.geo.goldstein_scale_trend(
                    country_code=country, mode="F"
                ),  # float, change vs prev period
                "battle_deaths_30d": lambda: self.geo.battle_deaths_30d(country_code=country, mode="F"),  # int
                "battle_deaths_90d": lambda: self.geo.battle_deaths_90d(country_code=country, mode="F"),  # int
                "protest_event_count_30d": lambda: self.geo.protest_event_count_30d(
                    country_code=country, mode="F"
                ),  # int
                "protest_violence_level": lambda: self.geo.protest_violence_level(
                    country_code=country, mode="F"
                ),  # float, 0-1
                "diplomatic_event_count_30d": lambda: self.geo.diplomatic_event_count_30d(
                    country_code=country, mode="F"
                ),  # int
                "diplomatic_intensity_avg": lambda: self.geo.diplomatic_intensity_avg(
                    country_code=country, mode="F"
                ),  # float, 0-10 scale
                "sanctions_count_active": lambda: self.geo.sanctions_count_active(country_code=country),  # int
                "sanctions_new_30d": lambda: self.geo.sanctions_new_30d(country_code=country),  # int
                "sanctions_sector_coverage": lambda: self.geo.sanctions_sector_coverage(
                    country_code=country
                ),  # float, 0-1
                "governance_wgi_composite": lambda: self.geo.governance_wgi_composite(
                    country_code=country, mode="F"
                ),  # float, -2.5 to +2.5
                "corruption_perception_index": lambda: self.geo.corruption_perception_index(
                    country_code=country, mode="F"
                ),  # int, 0-100
                "rule_of_law_score": lambda: self.geo.rule_of_law_score(
                    country_code=country, mode="F"
                ),  # float, -2.5 to +2.5
                "regulatory_quality": lambda: self.geo.regulatory_quality(
                    country_code=country, mode="F"
                ),  # float, -2.5 to +2.5
                "democracy_index": lambda: self.geo.democracy_index(country_code=country, mode="F"),  # float, 0-1
                "regime_type": lambda: self.geo.regime_type(
                    country_code=country, mode="F"
                ),  # string: democracy/hybrid/autocracy
                "press_freedom_score": lambda: self.geo.press_freedom_score(
                    country_code=country, mode="F"
                ),  # int, 0-100
            }
        )
        security = await _await_group(
            {
                "military_spending_gdp": lambda: self.sec.military_spending_gdp(
                    country_code=country, mode="F"
                ),  # float, percent
                "military_spending_growth_yoy": lambda: self.sec.military_spending_growth_yoy(
                    country_code=country, mode="F"
                ),  # float, percent
                "alliance_strength_score": lambda: self.sec.alliance_strength_score(
                    country_code=country, mode="F"
                ),  # float, 0-1
                "arms_imports_12m": lambda: self.sec.arms_imports_12m(
                    country_code=country, mode="F"
                ),  # int, millions USD
                "arms_exports_12m": lambda: self.sec.arms_exports_12m(
                    country_code=country, mode="F"
                ),  # int, millions USD
                "peacekeeping_troops": lambda: self.sec.peacekeeping_troops(country_code=country, mode="F"),  # int
                "nato_member": lambda: self.sec.nato_member(country_code=country),  # bool
            }
        )
        social = await _await_group(
            {
                "social_stability_index": lambda: self.soc.social_stability_index(
                    country_code=country, mode="F"
                ),  # float, 0-1
                "human_rights_score": lambda: self.soc.human_rights_score(country_code=country, mode="F"),  # float, 0-1
                "fragile_state_index": lambda: self.soc.fragile_state_index(
                    country_code=country, mode="F"
                ),  # float, 0-120
                "human_development_index": lambda: self.soc.human_development_index(
                    country_code=country, mode="F"
                ),  # float, 0-1
                "gini_coefficient": lambda: self.soc.gini_coefficient(country_code=country, mode="F"),  # float, 0-100
                "poverty_headcount_ratio": lambda: self.soc.poverty_headcount_ratio(
                    country_code=country, mode="F"
                ),  # float, percent
            }
        )
        environmental = await _await_group(
            {
                "climate_vulnerability_score": lambda: self.env.climate_vulnerability_score(
                    country_code=country, mode="F"
                ),  # float, 0-1
                "climate_readiness_score": lambda: self.env.climate_readiness_score(
                    country_code=country, mode="F"
                ),  # float, 0-1
                "natural_disaster_risk": lambda: self.env.natural_disaster_risk(
                    country_code=country, mode="F"
                ),  # float, 0-1
                "food_price_index_change_yoy": lambda: self.env.food_price_index_change_yoy(
                    country_code=country, mode="F"
                ),  # float, percent
                "energy_dependence_ratio": lambda: self.env.energy_dependence_ratio(
                    country_code=country, mode="F"
                ),  # float, 0-1 (imports/consumption)
                "water_stress_index": lambda: self.env.water_stress_index(country_code=country),  # float, 0-1
            }
        )
        return {
            "country": f"{country}",
            "economic": economic,
            "geopolitical": geopolitical,
            "security": security,
            "social": social,
            "environmental": environmental,
            "metadata": {
                "last_updated": f"{datetime.utcnow()}",
                "features_version": "1.0.0",
            },
        }

    async def build_training_panel(self, fns, countries) -> pl.DataFrame:
        panels = []

        for country in countries:
            series_dict = {}

            for fn in fns:
                try:
                    series = await fn(country, mode="ML")
                    if isinstance(series, pl.DataFrame) and not series.is_empty():
                        key = series.columns[0]
                        series = series.unique(subset=[key], keep="first")
                        series_dict[fn.__name__] = series
                except Exception as e:
                    logger.warning(f"{fn.__name__} failed for {country}: {e}")
                    continue

            if not series_dict:
                continue

            aligned: list[pl.DataFrame] = []
            for name, frame in series_dict.items():
                key = frame.columns[0]
                value_cols = [c for c in frame.columns if c != key]
                frame = frame.rename({key: "date"})
                for i, vc in enumerate(value_cols):
                    new_name = name if len(value_cols) == 1 else f"{name}_{vc}"
                    if new_name != vc:
                        frame = frame.rename({vc: new_name})
                frame = _normalize_key(frame, "date")
                frame = frame.sort("date").select(["date", *[c for c in frame.columns if c != "date"]])
                aligned.append(frame)

            country_df = aligned[0]
            for frame in aligned[1:]:
                country_df = country_df.join(frame, on="date", how="outer_coalesce")
            country_df = country_df.with_columns(pl.lit(country).alias("country_iso3"))
            country_df = country_df.select(["country_iso3", "date", *[c for c in country_df.columns if c not in ("country_iso3", "date")]])
            panels.append(country_df)

        if not panels:
            return pl.DataFrame()

        return pl.concat(panels, how="vertical").sort(["country_iso3", "date"])