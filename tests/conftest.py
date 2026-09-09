from __future__ import annotations

from pathlib import Path

import polars as pl
import pytest

from hermes.acquisition.cache import RawCache


@pytest.fixture
def tmp_cache(tmp_path: Path) -> RawCache:
    return RawCache(cache_dir=str(tmp_path / "hermes_cache"))


@pytest.fixture
def sample_wb_df() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "date": ["2023", "2022", "2021"],
            "indicator_id": ["NY.GDP.MKTP.KD.ZG"] * 3,
            "indicator_name": ["GDP growth (annual %)"] * 3,
            "country": ["USA"] * 3,
            "value": [2.5, 1.9, 5.8],
            "source": ["World_Bank"] * 3,
        }
    )


@pytest.fixture
def sample_wb_cpi_df() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "date": ["2023", "2022", "2021"],
            "indicator_id": ["FP.CPI.TOTL"] * 3,
            "indicator_name": ["Consumer price index"] * 3,
            "country": ["USA"] * 3,
            "value": [120.5, 117.8, 115.2],
            "source": ["World_Bank"] * 3,
        }
    )


@pytest.fixture
def sample_imf_df() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "date": ["2023", "2022", "2021"],
            "indicator_id": ["PPI.IX.A"] * 3,
            "indicator_name": ["Producer price index"] * 3,
            "country": ["USA"] * 3,
            "value": [110.0, 107.5, 105.0],
            "source": ["IMF"] * 3,
        }
    )


@pytest.fixture
def sample_fred_df() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "date": ["2023-10-01", "2023-07-01", "2023-04-01"],
            "value": ["27360.863", "27061.152", "26891.259"],
            "series_id": ["GDPC1"] * 3,
            "unit": ["Billions of Dollars"] * 3,
        }
    )


@pytest.fixture
def sample_binance_ohlcv():
    return [
        [
            1711900800000,
            "65000.00",
            "65500.00",
            "64800.00",
            "65200.00",
            "1000.00",
            1711904399999,
            "65000000.00",
            5000,
            "600.00",
            "400.00",
        ],
        [
            1711987200000,
            "65200.00",
            "66000.00",
            "65000.00",
            "65800.00",
            "1200.00",
            1711990799999,
            "78960000.00",
            6000,
            "700.00",
            "500.00",
        ],
    ]


@pytest.fixture
def sample_sec_xbrl():
    return {
        "facts": {
            "us-gaap": {
                "Revenues": {
                    "units": {
                        "USD": [{"val": 394328000000, "fy": 2023, "fp": "FY", "filed": "2023-10-27", "form": "10-K"}]
                    }
                },
                "CostOfRevenue": {"units": {"USD": [{"val": 214137000000}]}},
                "GrossProfit": {"units": {"USD": [{"val": 180191000000}]}},
                "NetIncomeLoss": {"units": {"USD": [{"val": 96995000000}]}},
                "EarningsPerShareBasic": {"units": {"USD/Shares": [{"val": 6.13}]}},
                "EarningsPerShareDiluted": {"units": {"USD/Shares": [{"val": 6.07}]}},
                "AssetsCurrent": {"units": {"USD": [{"val": 143534000000}]}},
                "Assets": {"units": {"USD": [{"val": 352755000000}]}},
                "LiabilitiesCurrent": {"units": {"USD": [{"val": 145308000000}]}},
                "Liabilities": {"units": {"USD": [{"val": 290437000000}]}},
                "StockholdersEquity": {"units": {"USD": [{"val": 62318000000}]}},
                "CashAndCashEquivalentsAtCarryingValue": {"units": {"USD": [{"val": 29943000000}]}},
                "OperatingIncomeLoss": {"units": {"USD": [{"val": 114301000000}]}},
                "NetCashProvidedByUsedInOperatingActivities": {"units": {"USD": [{"val": 110543000000}]}},
                "NetCashProvidedByUsedInInvestingActivities": {"units": {"USD": [{"val": -11493000000}]}},
                "NetCashProvidedByUsedInFinancingActivities": {"units": {"USD": [{"val": -89858000000}]}},
                "EntityCommonStockSharesOutstanding": {"units": {"shares": [{"val": 15534000000}]}},
            }
        }
    }
