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


class enviromental_features:
    def __init__(self):
        self.wb = World_bank()
        self._data = PUBLIC_DATASET()

    @feature(
        name="climate_vulnerability_score",
        group="enviromental_features",
        deps=["NDGAIN:cvs"],
        compute="climate vulnerability score computed from the NDGAIN dataset",
    )
    async def climate_vulnerability_score(
        self, country_code: str, mode: Literal["F", "ML"] = "F"
    ) -> float | pl.DataFrame:
        data = await self._data.fetch_cvs(country=country_code)
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
        name="climate_readiness_score",
        group="enviromental_features",
        deps=["NDGAIN:crs"],
        compute="climate readiness score computed from the NDGAIN dataset",
    )
    async def climate_readiness_score(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self._data.fetch_crs(country=country_code)
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

    @feature(name="natural_disaster_risk", group="enviromental_features", deps=[], compute="")
    async def natural_disaster_risk(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float: ...

    @feature(name="food_price_index_change_yoy", group="enviromental_features", deps=[], compute="")
    async def food_price_index_change_yoy(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float: ...

    @feature(name="energy_dependence_ratio", group="enviromental_features", deps=[], compute="")
    async def energy_dependence_ratio(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="EG.IMP.CONS.ZS")
        data = check_empty(mode=mode, data=data, country=country_code)
        if not isinstance(data, pl.DataFrame):
            return data
        if mode == "F":
            data = data.sort("date", descending=True)
            return data["value"].item(0)
        if mode == "ML":
            data = _to_year(data, "date")
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(name="water_stress_index", group="enviromental_features", deps=[], compute="")
    async def water_stress_index(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="ER.H2O.FWTL.ZS")
        data = check_empty(mode=mode, data=data, country=country_code)
        if not isinstance(data, pl.DataFrame):
            return data
        if mode == "F":
            data = data.sort("date", descending=True)
            return data["value"].item(0)
        if mode == "ML":
            data = _to_year(data, "date")
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])


if __name__ == "__main__":
    import asyncio

    async def main():
        env = enviromental_features()
        data = await env.water_stress_index(country_code="PAK")
        print(data)

    asyncio.run(main())
