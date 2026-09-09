from __future__ import annotations

from unittest.mock import AsyncMock, patch

import numpy as np
import polars as pl
import pytest

from hermes.constants import (
    BINANCE_INTERVAL_MAP,
    BINANCE_INTERVAL_MS,
    CANONICAL_FREQS,
    FINNHUB_MAX_DAYS,
    FINNHUB_RESOLUTION_MAP,
    YFINANCE_INTERVAL_MAP,
)
from hermes.features.financial.crpto import (
    CryptoHistory as TAHistory,
)
from hermes.features.financial.crpto import (
    _extract_funds_per_period,
    _extract_periods,
    _macd,
    _obv,
    _rolling_slope,
    _rsi,
)
from hermes.features.financial.filling import CompanyFiling as FAHistory


class TestFreqMappings:
    def test_all_canonical_freqs_mapped_to_binance(self):
        for freq in CANONICAL_FREQS:
            assert freq in BINANCE_INTERVAL_MAP, f"{freq} missing from BINANCE_INTERVAL_MAP"

    def test_binance_interval_ms_covers_all(self):
        for freq in CANONICAL_FREQS:
            assert freq in BINANCE_INTERVAL_MS, f"{freq} missing from BINANCE_INTERVAL_MS"

    def test_finnhub_resolution_map_covers_stock_freqs(self):
        stock_freqs = ["1m", "5m", "15m", "30m", "1h", "1d", "1w", "1M"]
        for freq in stock_freqs:
            assert freq in FINNHUB_RESOLUTION_MAP, f"{freq} missing from FINNHUB_RESOLUTION_MAP"

    def test_yfinance_interval_map_covers_stock_freqs(self):
        stock_freqs = ["1m", "5m", "15m", "30m", "1h", "1d", "1w", "1M"]
        for freq in stock_freqs:
            assert freq in YFINANCE_INTERVAL_MAP, f"{freq} missing from YFINANCE_INTERVAL_MAP"

    def test_finnhub_max_days_has_all_resolutions(self):
        for res in FINNHUB_RESOLUTION_MAP.values():
            assert res in FINNHUB_MAX_DAYS, f"Resolution {res!r} missing from FINNHUB_MAX_DAYS"

    def test_binance_ms_values_correct(self):
        assert BINANCE_INTERVAL_MS["1m"] == 60_000
        assert BINANCE_INTERVAL_MS["1h"] == 3_600_000
        assert BINANCE_INTERVAL_MS["1d"] == 86_400_000
        assert BINANCE_INTERVAL_MS["1w"] == 604_800_000


def _make_ohlcv_df(n: int = 250, start_price: float = 100.0) -> pl.DataFrame:
    np.random.seed(42)
    prices = start_price + np.cumsum(np.random.randn(n) * 0.5)
    prices = np.maximum(prices, 1.0)
    return pl.DataFrame(
        {
            "open_time": np.arange(n) * 86_400_000,
            "open": prices * 0.99,
            "high": prices * 1.02,
            "low": prices * 0.98,
            "close": prices,
            "volume": np.random.uniform(1000, 5000, n),
            "quote_volume": np.random.uniform(100000, 500000, n),
            "taker_buy_volume": np.random.uniform(500, 2500, n),
            "trades_count": np.random.randint(500, 5000, n),
        }
    )


class TestTAHistoryFeatures:
    def test_compute_features_output_columns(self):
        df = _make_ohlcv_df(250)
        df = df.with_columns(
            pl.lit("BTCUSDT").alias("symbol"),
            pl.lit("1d").alias("interval"),
        )
        result = TAHistory._compute_features(df)

        expected_cols = [
            "ret_1b",
            "ret_open_to_close",
            "ret_3b",
            "ret_5b",
            "ret_10b",
            "ret_20b",
            "ret_60b",
            "hl_range",
            "body_range",
            "dist_sma_20",
            "dist_sma_50",
            "dist_sma_200",
            "ema_diff_9_21",
            "ema_diff_21_50",
            "vol_20",
            "vol_60",
            "atr_14_norm",
            "volume_sma_20",
            "volume_rel_20",
            "taker_buy_vol_ratio",
            "rsi_14",
            "macd",
            "macd_signal",
            "macd_hist",
            "bb_upper",
            "bb_lower",
            "bb_width",
            "bb_pct",
            "obv",
            "returns_skew_20",
            "returns_kurt_20",
            "drawdown",
            "amihud_illiquidity",
            "return_mean_20",
            "return_std_20",
            "return_zscore_20",
            "return_zscore_60",
            "upper_wick",
            "lower_wick",
            "upper_wick_ratio",
            "lower_wick_ratio",
            "body_to_range",
            "price_zscore_20",
            "price_zscore_50",
            "price_zscore_200",
            "high_distance_20",
            "low_distance_20",
            "volume_zscore_20",
            "volume_zscore_60",
            "volume_change_1",
            "volume_change_5",
            "volume_trend_20",
            "vol_ratio_20_60",
            "vol_change_1",
            "vol_change_5",
            "atr_ratio",
            "rsi_change_1",
            "rsi_change_5",
            "macd_hist_change_1",
            "macd_hist_change_5",
            "macd_hist_zscore_20",
            "bb_width_change",
            "bb_width_zscore_20",
            "bb_pct_change",
            "buy_pressure_change",
            "trade_count_change",
            "trade_count_zscore_20",
            "avg_trade_size",
            "avg_trade_size_zscore_20",
            "drawdown_change",
            "drawdown_duration",
            "recovery_from_drawdown",
        ]
        for col in expected_cols:
            assert col in result.columns, f"Missing column: {col}"

    def test_compute_features_row_count(self):
        df = _make_ohlcv_df(250)
        df = df.with_columns(
            pl.lit("BTCUSDT").alias("symbol"),
            pl.lit("1d").alias("interval"),
        )
        result = TAHistory._compute_features(df)
        assert len(result) == 250

    def test_wick_ratios_bounded(self):
        df = _make_ohlcv_df(250)
        df = df.with_columns(
            pl.lit("BTCUSDT").alias("symbol"),
            pl.lit("1d").alias("interval"),
        )
        result = TAHistory._compute_features(df)
        valid_upper = result["upper_wick_ratio"].drop_nans()
        valid_lower = result["lower_wick_ratio"].drop_nans()
        assert (valid_upper >= 0).all() and (valid_upper <= 1).all()
        assert (valid_lower >= 0).all() and (valid_lower <= 1).all()

    def test_body_to_range_bounded(self):
        df = _make_ohlcv_df(250)
        df = df.with_columns(
            pl.lit("BTCUSDT").alias("symbol"),
            pl.lit("1d").alias("interval"),
        )
        result = TAHistory._compute_features(df)
        valid = result["body_to_range"].drop_nans()
        assert (valid >= 0).all() and (valid <= 1).all()

    def test_rsi_bounded(self):
        closes = 100.0 + np.cumsum(np.random.randn(100) * 0.5)
        rsi = _rsi(closes, 14)
        valid = rsi[~np.isnan(rsi)]
        assert len(valid) > 0
        assert valid.min() >= 0
        assert valid.max() <= 100

    def test_macd_returns_three_arrays(self):
        closes = 100.0 + np.cumsum(np.random.randn(100) * 0.5)
        macd, signal, hist = _macd(closes)
        assert len(macd) == len(closes)
        assert len(signal) == len(closes)
        assert len(hist) == len(closes)

    def test_obv_monotonic_increasing_uptrend(self):
        closes = np.arange(1.0, 51.0)
        volumes = np.ones(50) * 100
        obv = _obv(closes, volumes)
        assert np.all(np.diff(obv) >= 0)

    def test_drawdown_always_non_positive(self):
        df = _make_ohlcv_df(250)
        df = df.with_columns(
            pl.lit("BTCUSDT").alias("symbol"),
            pl.lit("1d").alias("interval"),
        )
        result = TAHistory._compute_features(df)
        valid = result["drawdown"].drop_nans()
        assert (valid <= 0).all()

    def test_drawdown_duration_non_negative(self):
        df = _make_ohlcv_df(250)
        df = df.with_columns(
            pl.lit("BTCUSDT").alias("symbol"),
            pl.lit("1d").alias("interval"),
        )
        result = TAHistory._compute_features(df)
        valid = result["drawdown_duration"].drop_nans()
        assert (valid >= 0).all()

    def test_recovery_from_drawdown_bounded(self):
        df = _make_ohlcv_df(250)
        df = df.with_columns(
            pl.lit("BTCUSDT").alias("symbol"),
            pl.lit("1d").alias("interval"),
        )
        result = TAHistory._compute_features(df)
        valid = result["recovery_from_drawdown"].drop_nans()
        assert (valid >= 0).all() and (valid <= 1).all()

    def test_price_zscore_20_bounded_reasonably(self):
        df = _make_ohlcv_df(250)
        df = df.with_columns(
            pl.lit("BTCUSDT").alias("symbol"),
            pl.lit("1d").alias("interval"),
        )
        result = TAHistory._compute_features(df)
        valid = result["price_zscore_20"].drop_nans()
        assert valid.abs().max() < 10

    def test_rolling_slope(self):
        series = pl.Series(np.arange(20.0))
        result = _rolling_slope(series, 5)
        assert not np.isnan(result[-1])
        assert result[-1] == pytest.approx(1.0, abs=0.01)

    def test_volume_change_non_negative(self):
        df = _make_ohlcv_df(250)
        df = df.with_columns(
            pl.lit("BTCUSDT").alias("symbol"),
            pl.lit("1d").alias("interval"),
        )
        result = TAHistory._compute_features(df)
        valid = result["volume_change_1"].drop_nans()
        assert (valid >= -1).all()

    def test_avg_trade_size_positive(self):
        df = _make_ohlcv_df(250)
        df = df.with_columns(
            pl.lit("BTCUSDT").alias("symbol"),
            pl.lit("1d").alias("interval"),
        )
        result = TAHistory._compute_features(df)
        valid = result["avg_trade_size"].drop_nans()
        assert (valid > 0).all()


class TestTAHistoryAsync:
    async def test_get_history_empty(self):
        ta = TAHistory()
        with patch.object(ta.binance, "fetch_history", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = pl.DataFrame()
            result = await ta.get_history("BTCUSDT", interval="1d", years=1)
            assert result.is_empty()

    async def test_get_history_calls_features(self):
        ta = TAHistory()
        mock_df = _make_ohlcv_df(250)
        with patch.object(ta.binance, "fetch_history", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_df
            result = await ta.get_history("BTCUSDT", interval="1d", years=1)
            assert not result.is_empty()
            assert "rsi_14" in result.columns
            assert "macd" in result.columns
            assert "drawdown_duration" in result.columns
            mock_fetch.assert_called_once()


class TestFundamentalFeatures:
    def _make_filing_df(self) -> pl.DataFrame:
        return pl.DataFrame(
            [
                {
                    "ticker": "AAPL",
                    "filing_date": "2024-10-25",
                    "fiscal_period": "Q1",
                    "fiscal_year": 2024,
                    "filing_type": "10-Q",
                    "revenue": 94930,
                    "cost_of_revenue": 56380,
                    "gross_profit": 38550,
                    "operating_expenses": 14380,
                    "operating_income": 24170,
                    "interest_expense": 2800,
                    "pre_tax_income": 27100,
                    "income_tax_expense": 3600,
                    "net_income": 23500,
                    "eps_basic": 1.57,
                    "eps_diluted": 1.55,
                    "cash": 29940,
                    "short_term_investments": 0,
                    "accounts_receivable": 66000,
                    "inventory": 6500,
                    "current_assets": 143534,
                    "total_assets": 352755,
                    "current_liabilities": 145308,
                    "short_term_debt": 15200,
                    "long_term_debt": 97000,
                    "total_liabilities": 290437,
                    "equity": 62318,
                    "operating_cash_flow": 110543,
                    "investing_cash_flow": -11493,
                    "financing_cash_flow": -89858,
                    "capital_expenditure": 9450,
                    "shares_outstanding": 15534,
                    "weighted_average_shares": 15534,
                    "dividends": 3800,
                    "buybacks": 25000,
                },
                {
                    "ticker": "AAPL",
                    "filing_date": "2023-10-27",
                    "fiscal_period": "Q1",
                    "fiscal_year": 2023,
                    "filing_type": "10-K",
                    "revenue": 89498,
                    "cost_of_revenue": 53266,
                    "gross_profit": 36232,
                    "operating_expenses": 13900,
                    "operating_income": 22332,
                    "interest_expense": 2600,
                    "pre_tax_income": 25000,
                    "income_tax_expense": 3300,
                    "net_income": 21700,
                    "eps_basic": 1.43,
                    "eps_diluted": 1.41,
                    "cash": 28500,
                    "short_term_investments": 0,
                    "accounts_receivable": 62000,
                    "inventory": 6000,
                    "current_assets": 135000,
                    "total_assets": 340000,
                    "current_liabilities": 138000,
                    "short_term_debt": 14500,
                    "long_term_debt": 95000,
                    "total_liabilities": 280000,
                    "equity": 60000,
                    "operating_cash_flow": 100000,
                    "investing_cash_flow": -10000,
                    "financing_cash_flow": -85000,
                    "capital_expenditure": 8500,
                    "shares_outstanding": 15800,
                    "weighted_average_shares": 15800,
                    "dividends": 3500,
                    "buybacks": 22000,
                },
            ]
        )

    def _row_2024(self, result: pl.DataFrame) -> pl.DataFrame:
        return result.filter(pl.col("fiscal_year") == 2024).row(0, named=True)

    def test_compute_fundamental_features_growth(self):
        df = self._make_filing_df()
        result = FAHistory._compute_fundamental_features(df)
        assert "revenue_growth_yoy" in result.columns
        row = self._row_2024(result)
        expected = (94930 - 89498) / 89498
        assert row["revenue_growth_yoy"] == pytest.approx(expected, rel=1e-4)

    def test_compute_fundamental_features_margins(self):
        df = self._make_filing_df()
        result = FAHistory._compute_fundamental_features(df)
        assert "gross_margin" in result.columns
        assert "operating_margin" in result.columns
        assert "net_margin" in result.columns
        assert "ocf_margin" in result.columns
        row = self._row_2024(result)
        assert row["gross_margin"] == pytest.approx(38550 / 94930, rel=1e-4)

    def test_compute_fundamental_features_liquidity(self):
        df = self._make_filing_df()
        result = FAHistory._compute_fundamental_features(df)
        assert "current_ratio" in result.columns
        assert "quick_ratio" in result.columns
        assert "cash_ratio" in result.columns

    def test_compute_fundamental_features_leverage(self):
        df = self._make_filing_df()
        result = FAHistory._compute_fundamental_features(df)
        assert "debt_to_equity" in result.columns
        assert "debt_to_assets" in result.columns
        assert "net_debt" in result.columns

    def test_compute_fundamental_features_cash_flow(self):
        df = self._make_filing_df()
        result = FAHistory._compute_fundamental_features(df)
        assert "free_cash_flow" in result.columns
        assert "fcf_margin" in result.columns
        assert "capex_to_revenue" in result.columns
        row = self._row_2024(result)
        assert row["free_cash_flow"] == pytest.approx(110543 - 9450, rel=1e-4)

    def test_compute_fundamental_features_shareholder(self):
        df = self._make_filing_df()
        result = FAHistory._compute_fundamental_features(df)
        assert "share_count_change_yoy" in result.columns
        assert "buyback_to_net_income" in result.columns
        assert "dividend_to_net_income" in result.columns

    def test_compute_fundamental_features_coverage(self):
        df = self._make_filing_df()
        result = FAHistory._compute_fundamental_features(df)
        assert "interest_coverage" in result.columns
        row = self._row_2024(result)
        assert row["interest_coverage"] == pytest.approx(24170 / 2800, rel=1e-4)

    def test_compute_fundamental_empty_df(self):
        result = FAHistory._compute_fundamental_features(pl.DataFrame())
        assert result.is_empty()

    def test_compute_fundamental_single_row(self):
        df = self._make_filing_df().slice(0, 1)
        result = FAHistory._compute_fundamental_features(df)
        assert len(result) == 1


class TestExtractPeriods:
    def _make_facts(self) -> dict:
        return {
            "Revenues": {
                "units": {
                    "USD": [
                        {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 94930},
                        {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 89498},
                        {"fy": 2023, "fp": "Q4", "filed": "2024-01-26", "form": "10-K", "val": 119575},
                    ]
                }
            }
        }

    def test_extract_periods_returns_correct_count(self):
        facts = self._make_facts()
        result = _extract_periods(facts, quarters=2)
        assert len(result) == 2

    def test_extract_periods_sorted_descending(self):
        facts = self._make_facts()
        result = _extract_periods(facts, quarters=3)
        assert result[0]["fiscal_year"] >= result[1]["fiscal_year"]

    def test_extract_periods_empty_facts(self):
        result = _extract_periods({}, quarters=8)
        assert result == []

    def test_extract_funds_per_period(self):
        facts = self._make_facts()
        periods = _extract_periods(facts, quarters=2)
        result = _extract_funds_per_period(facts, periods, "AAPL")
        assert len(result) == 2
        assert all(r["ticker"] == "AAPL" for r in result)
        assert all("revenue" in r for r in result)


class TestFAHistoryAsync:
    async def test_get_history_empty(self):
        fa = FAHistory(finnhub_api="test", sec_email="test", sec_username="test", fred_api="test")
        with patch.object(fa.sec, "fetch", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = None
            result = await fa.get_history(quarters=2, symbols=["AAPL"])
            assert result.is_empty()

    async def test_get_history_calls_sec(self):
        fa = FAHistory(finnhub_api="test", sec_email="test", sec_username="test", fred_api="test")
        mock_raw = {
            "facts": {
                "us-gaap": {
                    "Revenues": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 94930},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 89498},
                            ]
                        }
                    },
                    "GrossProfit": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 38550},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 36232},
                            ]
                        }
                    },
                    "OperatingIncomeLoss": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 24170},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 22332},
                            ]
                        }
                    },
                    "NetIncomeLoss": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 23500},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 21700},
                            ]
                        }
                    },
                    "EarningsPerShareDiluted": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 1.55},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 1.41},
                            ]
                        }
                    },
                    "AssetsCurrent": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 143534},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 135000},
                            ]
                        }
                    },
                    "LiabilitiesCurrent": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 145308},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 138000},
                            ]
                        }
                    },
                    "Assets": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 352755},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 340000},
                            ]
                        }
                    },
                    "StockholdersEquity": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 62318},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 60000},
                            ]
                        }
                    },
                    "CashAndCashEquivalentsAtCarryingValue": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 29940},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 28500},
                            ]
                        }
                    },
                    "InventoryNet": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 6500},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 6000},
                            ]
                        }
                    },
                    "AccountsReceivableNetCurrent": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 66000},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 62000},
                            ]
                        }
                    },
                    "LongTermDebtNoncurrent": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 97000},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 95000},
                            ]
                        }
                    },
                    "ShortTermDebtCurrent": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 15200},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 14500},
                            ]
                        }
                    },
                    "Liabilities": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 290437},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 280000},
                            ]
                        }
                    },
                    "NetCashProvidedByUsedInOperatingActivities": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 110543},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 100000},
                            ]
                        }
                    },
                    "PaymentsToAcquirePropertyPlantAndEquipment": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 9450},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 8500},
                            ]
                        }
                    },
                    "EntityCommonStockSharesOutstanding": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 15534},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 15800},
                            ]
                        }
                    },
                    "PaymentsOfDividends": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 3800},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 3500},
                            ]
                        }
                    },
                    "PaymentsForRepurchaseOfCommonStock": {
                        "units": {
                            "USD": [
                                {"fy": 2024, "fp": "Q1", "filed": "2024-10-25", "form": "10-Q", "val": 25000},
                                {"fy": 2023, "fp": "Q1", "filed": "2023-10-27", "form": "10-K", "val": 22000},
                            ]
                        }
                    },
                }
            }
        }
        with patch.object(fa.sec, "fetch", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_raw
            result = await fa.get_history(quarters=2, symbols=["AAPL"])
            assert not result.is_empty()
            assert "revenue" in result.columns
            assert "gross_margin" in result.columns


class TestBinanceBuildUrlWithTime:
    def test_ohlcv_with_start_end_time(self):
        from hermes.connectors.binance import Binance

        b = Binance(cache=None)
        url, params = b._build_url(
            "spot",
            "ohlcv",
            "BTCUSDT",
            interval="1d",
            limit="1000",
            start_time=1700000000000,
            end_time=1700100000000,
        )
        assert params["startTime"] == 1700000000000
        assert params["endTime"] == 1700100000000
        assert params["symbol"] == "BTCUSDT"

    def test_ohlcv_without_time_params(self):
        from hermes.connectors.binance import Binance

        b = Binance(cache=None)
        url, params = b._build_url(
            "spot",
            "ohlcv",
            "BTCUSDT",
            interval="1d",
            limit="100",
        )
        assert "startTime" not in params
        assert "endTime" not in params
