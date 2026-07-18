from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


STD_COLUMNS = ["date", "country", "indicator", "value", "source"]
STD_DTYPES = {
    "date": "datetime64[ns]",
    "country": "object",
    "indicator": "object",
    "value": "float64",
    "source": "object",
}


def ensure_std_schema(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    for col in STD_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col!r}")
    df = df[STD_COLUMNS].copy()
    df["date"] = pd.to_datetime(df["date"])
    df["country"] = df["country"].astype(str).str.upper()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["source"] = source_name
    return df


class BaseConnector(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def fetch(self, **kwargs) -> pd.DataFrame: ...

    def normalize(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        return ensure_std_schema(df, self.name)

    def validate(self, df: pd.DataFrame) -> bool:
        for col in STD_COLUMNS:
            if col not in df.columns:
                return False
        return True

    def get_available_countries(self) -> list[str]:
        return []

    def get_date_range(self, country: str) -> tuple[str, str]:
        return ("", "")
