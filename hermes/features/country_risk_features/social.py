import logging
from typing import Literal

import polars as pl

from hermes.connectors.public_data import PUBLIC_DATASET
from hermes.connectors.world_bank import World_bank
from hermes.features.country_risk_features.utils import adjust_year_range, check_empty
from hermes.features.decorator import feature

logger = logging.getLogger(__name__)


def _to_year(df: pl.DataFrame, col: str) -> pl.DataFrame:
    if df.schema[col] in (pl.Date, pl.Datetime, pl.Time):
        year = pl.col(col).dt.year()
    else:
        year = pl.col(col).str.to_date("%Y").dt.year()
    return df.with_columns(year.alias("year"))


class social_features:
    def __init__(self):
        self.wb = World_bank()
        self._data = PUBLIC_DATASET()

    @feature(
        name="social_stability_index",
        group="social_features",
        deps=[],
        compute="social_stability_index",
    )
    async def social_stability_index(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float: ...

    @feature(
        name="human_rights_score",
        group="social_features",
        deps=["hrs:human_rights"],
        compute="human_rights_score from the Human Rights Score dataset",
    )
    async def human_rights_score(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self._data.fetch_hrs(country=country_code)
        data = check_empty(data=data, mode=mode)
        if not isinstance(data, pl.DataFrame):
            return data
        if mode == "F":
            data = data.sort("date", descending=True)
            return data["human_right_score"].item(0)
        if mode == "ML":
            data = _to_year(data, "date")
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "human_right_score"])

    @feature(
        name="fragile_state_index",
        group="social_features",
        deps=["fsi:fragile_states"],
        compute="fragile_state_index from the Fragile States Index dataset",
    )
    async def fragile_state_index(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self._data.fetch_fsi(country=country_code)
        data = check_empty(data=data, mode=mode)
        if not isinstance(data, pl.DataFrame):
            return data
        if mode == "F":
            data = data.sort("date", descending=True)
            return data["Total"].item(0)
        if mode == "ML":
            data = _to_year(data, "date")
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "Total"])

    @feature(
        name="human_development_index",
        group="social_features",
        deps=["hdi:human_development"],
        compute="human_development_index from the HDI dataset",
    )
    async def human_development_index(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self._data.fetch_hdi(country=country_code)
        data = check_empty(data=data, mode=mode)
        if not isinstance(data, pl.DataFrame):
            return data
        if mode == "F":
            data = data.sort("year", descending=True)
            return data["score"].item(0)
        if mode == "ML":
            data = _to_year(data, "year")
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["year", "score"])

    @feature(
        name="gini_coefficient",
        group="social_features",
        deps=["world_bank:SI.POV.GINI"],
        compute="gini_coefficient from the World Bank data",
    )
    async def gini_coefficient(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="SI.POV.GINI")
        data = check_empty(data=data, mode=mode)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            data = data.sort("date", descending=True)
            return data["value"].item(0)
        if mode == "ML":
            data = _to_year(data, "date")
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="poverty_headcount_ratio",
        group="social_features",
        deps=["world_bank:SI.POV.DDAY"],
        compute="poverty_headcount_ratio from the World Bank data",
    )
    async def poverty_headcount_ratio(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="SI.POV.DDAY")
        data = check_empty(data=data, mode=mode)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            data = data.sort("date", descending=True)
            return data["value"].item(0)
        if mode == "ML":
            data = _to_year(data, "date")
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])