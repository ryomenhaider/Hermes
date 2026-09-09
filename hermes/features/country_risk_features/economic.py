import logging
from datetime import date
from typing import Literal

import polars as pl

from hermes.connectors.imf import IMF
from hermes.connectors.world_bank import World_bank
from hermes.features.country_risk_features.utils import adjust_year_range, check_empty
from hermes.features.decorator import feature

logger = logging.getLogger(__name__)


def _year_date(df, date_col: str = "date") -> pl.DataFrame:
    """Convert a year-string column (e.g. "2023") to a date and derive a year int column."""
    return df.with_columns(
        pl.col(date_col).str.to_date("%Y").alias(date_col),
        pl.col(date_col).str.to_date("%Y").dt.year().alias("year"),
    )


def _year_end(df, date_col: str = "date") -> pl.DataFrame:
    """Anchor a year-string column (e.g. "2023") to Dec 31 of that year as a date."""
    return df.with_columns(
        (pl.col(date_col).cast(pl.Utf8) + "-12-31").str.to_date("%Y-%m-%d").alias(date_col)
    )


class economic_features:
    def __init__(self):
        self.wb = World_bank()
        self.imf = IMF()

    @feature(
        name="gdp_growth_yoy",
        group="economic_features",
        deps=["world_bank:NY.GDP.MKTP.KD.ZG"],
        compute="GDP growth YoY, merged from WB and IMF",
    )
    async def gdp_growth_yoy(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="NY.GDP.MKTP.KD.ZG")
        data = check_empty(mode=mode, data=data, country=country_code)
        if not isinstance(data, pl.DataFrame):
            return data
        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="gdp_growth_qoq",
        group="economic_features",
        deps=["world_bank:NY.GDP.MKTP.KD"],
        compute="GDP growth QoQ, interpolated from the annual frequency data from the World_Bank",
    )
    async def gdp_growth_qoq(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="NY.GDP.MKTP.KD")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        data = _year_end(data)

        min_year = data["date"].dt.year().min()
        max_year = data["date"].dt.year().max()
        grid_dates = [
            date(year, month, day)
            for year in range(min_year, max_year + 1)
            for month, day in [(3, 31), (6, 30), (9, 30), (12, 31)]
        ]
        grid = pl.DataFrame({"date": grid_dates}).sort("date")
        df = grid.join(data.select(["date", "value"]), on="date", how="left")
        df = df.with_columns(pl.col("value").interpolate())
        df = df.with_columns((pl.col("value").pct_change() * 100).alias("gdp_growth_qoq")).drop("value")

        if mode == "F":
            return float(df["gdp_growth_qoq"].fill_null(float("nan")).item(0))
        if mode == "ML":
            return df.select(["date", "gdp_growth_qoq"])

    @feature(
        name="industrial_production_yoy",
        group="economic_features",
        deps=["world_bank:NV.IND.MANF.KD.ZG"],
        compute="industrial_production_yoy from the World Bank data",
    )
    async def industrial_production_yoy(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="NV.IND.MANF.KD.ZG")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))

        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="inflation_cpi_yoy",
        group="economic_features",
        deps=["world_bank:FP.CPI.TOTL.ZG"],
        compute="inflation_cpi_yoy from the World Bank data",
    )
    async def inflation_cpi_yoy(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="FP.CPI.TOTL.ZG")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))

        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="inflation_volatility_12m",
        group="economic_features",
        deps=["world_bank:FP.CPI.TOTL"],
        compute="inflation_volatility_12m from the World Bank data",
    )
    async def inflation_volatility_12m(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="FP.CPI.TOTL")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        data = _year_end(data)
        data = data.sort("date").with_columns(pl.col("date").dt.month_start())

        min_date = data["date"].min()
        max_date = data["date"].max()
        grid_dates = [
            date(year, month, 1)
            for year in range(min_date.year, max_date.year + 1)
            for month in range(1, 13)
        ]
        grid = pl.DataFrame({"date": grid_dates}).sort("date")
        monthly = grid.join(data.select(["date", "value"]), on="date", how="left")
        monthly = monthly.with_columns(pl.col("value").interpolate())
        monthly = monthly.with_columns(
            pl.col("value")
            .pct_change(12)
            .alias("yoy_change")
        )
        monthly = monthly.with_columns(
            pl.col("yoy_change").rolling_std(12).alias("inflation_volatility_12m")
        ).drop("yoy_change")

        result = monthly.filter(pl.col("inflation_volatility_12m").is_not_null()).sort("date", descending=True)

        if mode == "F":
            return float(result["inflation_volatility_12m"].item(0))
        if mode == "ML":
            result = _year_date(result)
            result = adjust_year_range(result, "year", 2000, 2025, fill_method="ffill")
            return result.select(["date", "inflation_volatility_12m"])

    @feature(
        name="ppi_yoy",
        group="economic_features",
        deps=["IMF:IMF.STA:PPI:PPI.IX.A"],
        compute="ppi_yoy from the IMF data",
    )
    async def ppi_yoy(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.imf.fetch(country=country_code, agency="IMF.STA", dataflow_id="PPI", key="PPI.IX.A")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="inflation_yoy",
        group="economic_features",
        deps=["world_bank:NV.IND.MANF.KD.ZG"],
        compute="inflation_yoy from the IMF data",
    )
    async def inflation_yoy(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.imf.fetch(country=country_code, agency="IMF.STA", dataflow_id="CPI", key="CPI._T.IX.M")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="unemployment_rate",
        group="economic_features",
        deps=["world_bank:SL.UEM.TOTL.ZS"],
        compute="unemployment_rate from the World Bank data",
    )
    async def unemployment_rate(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="SL.UEM.TOTL.ZS")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="youth_unemployment",
        group="economic_features",
        deps=["world_bank:SL.UEM.1524.ZS"],
        compute="youth_unemployment from the World Bank data",
    )
    async def youth_unemployment(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="SL.UEM.1524.ZS")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="labor_force_participation",
        group="economic_features",
        deps=["world_bank:SL.TLF.CACT.ZS"],
        compute="labor_force_participation from the World Bank data",
    )
    async def labor_force_participation(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="SL.TLF.CACT.ZS")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="current_account_gdp_ratio",
        group="economic_features",
        deps=["world_bank:BN.CAB.XOKA.GD.ZS"],
        compute="current_account_gdp_ratio from the World Bank data",
    )
    async def current_account_gdp_ratio(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="BN.CAB.XOKA.GD.ZS")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="fx_reserves_months_import",
        group="economic_features",
        deps=["world_bank:FI.RES.TOTL.MO"],
        compute="fx_reserves_months_import from the World Bank data",
    )
    async def fx_reserves_months_import(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="FI.RES.TOTL.MO")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="external_debt_gdp_ratio",
        group="economic_features",
        deps=["world_bank:DT.DOD.DECT.GN.ZS"],
        compute="external_debt_gdp_ratio from the World Bank data",
    )
    async def external_debt_gdp_ratio(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="DT.DOD.DECT.GN.ZS")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="fiscal_deficit_gdp",
        group="economic_features",
        deps=["IMF:IMF.RES:WEO:GGXCNL_NGDP"],
        compute="fiscal_deficit_gdp from the IMF data",
    )
    async def fiscal_deficit_gdp(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.imf.fetch(country=country_code, agency="IMF.RES", dataflow_id="WEO", key="GGXCNL_NGDP")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="government_debt_gdp",
        group="economic_features",
        deps=["IMF:IMF.RES:WEO:GGXWDG_NGDP"],
        compute="government_debt_gdp from the IMF data",
    )
    async def government_debt_gdp(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.imf.fetch(country=country_code, agency="IMF.RES", dataflow_id="WEO", key="GGXWDG_NGDP")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="reer_misalignment",
        group="economic_features",
        deps=["IMF:IMF.STA:ER:EREER_IX.M"],
        compute="reer_misalignment from the IMF data",
    )
    async def reer_misalignment(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.imf.fetch(country=country_code, agency="IMF.STA", dataflow_id="ER", key="EREER_IX.M")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="banking_sector_health",
        group="economic_features",
        deps=["world_bank:FB.AST.NPLN.ZS"],
        compute="banking_sector_health from the World Bank data",
    )
    async def banking_sector_health(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="FB.AST.NPLN.ZS")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])

    @feature(
        name="gdp_per_capita_ppp",
        group="economic_features",
        deps=["world_bank:NY.GDP.PCAP.PP.CD"],
        compute="gdp_per_capita_ppp from the World Bank data",
    )
    async def gdp_per_capita_ppp(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pl.DataFrame:
        data = await self.wb.fetch(country_code=country_code, indicator_code="NY.GDP.PCAP.PP.CD")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pl.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].item(0))
        if mode == "ML":
            data = _year_date(data)
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            return data.select(["date", "value"])


if __name__ == "__main__":
    import asyncio

    async def main():
        eco = economic_features()
        data = await eco.inflation_volatility_12m("USA", "ML")
        data.write_csv("data/data.csv")
        print(data)

    asyncio.run(main())