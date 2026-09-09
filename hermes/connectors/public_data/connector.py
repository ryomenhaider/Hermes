import asyncio
from pathlib import Path

import polars as pl

CURRENT_DIR = Path(__file__).resolve().parent.parent

HRS_PATH = CURRENT_DIR / "lib" / "datasets" / "hrs.csv"
HDI_PATH = CURRENT_DIR / "lib" / "datasets" / "hdi1.csv"
CPI_PATH = CURRENT_DIR / "lib" / "datasets" / "global_cpi_all.csv"
FSI_PATH = CURRENT_DIR / "lib" / "datasets" / "fsi.csv"
NATO_PATH = CURRENT_DIR / "lib" / "datasets" / "nato.csv"
CRS_PATH = CURRENT_DIR / "lib" / "datasets" / "crs.csv"
CVS_PATH = CURRENT_DIR / "lib" / "datasets" / "cvs.csv"
SIPRI_PATH = CURRENT_DIR / "lib" / "datasets" / "sipri.csv"


class PUBLIC_DATASET:
    async def fetch_hrs(self, country: str) -> pl.DataFrame:
        df = await asyncio.to_thread(pl.read_csv, HRS_PATH)
        data = df.filter(pl.col("country") == country)
        data = data.with_columns(pl.col("date").str.to_date())
        return data

    async def fetch_hdi(self, country: str) -> pl.DataFrame:
        df = await asyncio.to_thread(pl.read_csv, HDI_PATH)
        df.columns = [c if c != "" else "index" for c in df.columns]
        data = df.select(["country", "Year", "HDI"])
        data.columns = ["iso3", "year", "score"]
        data = data.with_columns(pl.col("year").cast(pl.Utf8).str.to_date())
        data = data.filter(pl.col("iso3") == country)
        return data

    async def fetch_cpi(self, country: str) -> pl.DataFrame:
        df = await asyncio.to_thread(pl.read_csv, CPI_PATH)
        data = df.select(["iso3", "year", "score"])
        data = data.with_columns(pl.col("year").cast(pl.Utf8).str.to_date())
        data = data.filter(pl.col("iso3") == country)
        return data

    async def fetch_fsi(self, country: str) -> pl.DataFrame:
        df = await asyncio.to_thread(pl.read_csv, FSI_PATH)
        data = df.filter(pl.col("country") == country)
        data = data.with_columns(pl.col("date").str.to_date())
        return data

    async def fetch_nato(self, country: str) -> pl.DataFrame:
        df = await asyncio.to_thread(pl.read_csv, NATO_PATH)
        data = df.filter(pl.col("ISO3") == country)
        data = data.with_columns(pl.col("Year").cast(pl.Utf8).str.to_date())
        return data

    async def fetch_crs(self, country: str) -> pl.DataFrame:
        df = await asyncio.to_thread(pl.read_csv, CRS_PATH)
        data = df.filter(pl.col("ISO3") == country)
        data = data.with_columns(pl.col("year").cast(pl.Utf8).str.to_date())
        return data

    async def fetch_cvs(self, country: str) -> pl.DataFrame:
        df = await asyncio.to_thread(pl.read_csv, CVS_PATH)
        data = df.filter(pl.col("ISO3") == country)
        data = data.with_columns(pl.col("year").cast(pl.Utf8).str.to_date())
        return data

    async def fetch_sipri(self, country: str) -> pl.DataFrame:
        df = await asyncio.to_thread(pl.read_csv, SIPRI_PATH)
        data = df.filter(pl.col("iso3") == country)
        data = data.with_columns(pl.col("year").cast(pl.Utf8).str.to_date())
        return data
