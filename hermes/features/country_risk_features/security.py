import logging
from typing import Literal

import polars as pl

from hermes.connectors.public_data import PUBLIC_DATASET
from hermes.features.country_risk_features.utils import adjust_year_range
from hermes.features.decorator import feature

logger = logging.getLogger(__name__)


def _year_int(df, year_col: str) -> pl.DataFrame:
    return df.with_columns(pl.col(year_col).dt.year().alias(year_col))


class security_features:
    def __init__(self):
        self._data = PUBLIC_DATASET()

    @feature(
        name="military_spending_gdp",
        group="security_features",
        deps=["sipri:milex"],
        compute="military_spending_gdp from the SIPRI dataset",
    )
    async def military_spending_gdp(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self._data.fetch_sipri(country=country_code)
        data = _year_int(data, "year")

        if mode == "F":
            data = data.sort("year", descending=True)
            return float(data["value"].item(0))
        if mode == "ML":
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["year", "value"])

    @feature(
        name="military_spending_growth_yoy",
        group="security_features",
        deps=["sipri:milex"],
        compute="military_spending_growth_yoy from the SIPRI dataset",
    )
    async def military_spending_growth_yoy(
        self, country_code: str, mode: Literal["F", "ML"] = "F"
    ) -> float | pl.DataFrame:

        data = await self._data.fetch_sipri(country=country_code)
        data = _year_int(data, "year")
        data = data.sort("year", descending=True)

        yoy = data.with_columns((pl.col("value").pct_change() * 100).alias("value_yoy")).drop("value")

        if mode == "F":
            latest = yoy.filter(pl.col("value_yoy").is_not_null()).sort("year", descending=True)
            if latest.is_empty():
                return float("nan")
            if latest.height < 2:
                return float("nan")
            return float(latest["value_yoy"].item(1))
        if mode == "ML":
            yoy = yoy.with_columns(pl.col("value_yoy").alias("value")).drop("value_yoy")
            yoy = adjust_year_range(yoy, "year", 2000, 2025, fill_method="ffill")
            return yoy.select(["year", "value"])

        raise ValueError(f"Unsupported mode: {mode!r}")

    @feature(
        name="alliance_strength_score",
        group="security_features",
        deps=[],
        compute="alliance_strength_score",
    )
    async def alliance_strength_score(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float:
        pass

    @feature(
        name="arms_imports_12m",
        group="security_features",
        deps=[],
        compute="arms_imports_12m",
    )
    async def arms_imports_12m(self, country_code: str, mode: Literal["F", "ML"] = "F") -> int:
        pass

    @feature(
        name="arms_exports_12m",
        group="security_features",
        deps=[],
        compute="arms_exports_12m",
    )
    async def arms_exports_12m(self, country_code: str, mode: Literal["F", "ML"] = "F") -> int:
        pass

    @feature(
        name="peacekeeping_troops",
        group="security_features",
        deps=[],
        compute="peacekeeping_troops",
    )
    async def peacekeeping_troops(self, country_code: str, mode: Literal["F", "ML"] = "F") -> int:
        pass

    @feature(
        name="nato_member",
        group="security_features",
        deps=["nato:membership"],
        compute="nato_member from the NATO dataset",
    )
    async def nato_member(self, country_code: str, mode: Literal["F", "ML"] = "F") -> bool | pl.DataFrame:
        data = await self._data.fetch_nato(country=country_code)
        data = _year_int(data, "Year")

        if mode == "F":
            data = data.sort("Year", descending=True)
            return bool(data["NATO Member"].item(0))
        elif mode == "ML":
            data = adjust_year_range(data, "Year", 2000, 2025, fill_method="ffill")
            return data.select(["Year", "NATO Member"])