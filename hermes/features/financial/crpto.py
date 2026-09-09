import logging

import numpy as np
import polars as pl

from hermes.connectors.binance import Binance
from hermes.connectors.sec.tags import SEC_TAG_MAP

logger = logging.getLogger(__name__)


class CryptoHistory:
    def __init__(self):
        self.binance = Binance()

    async def get_history(
        self,
        symbol: str,
        interval: str = "1d",
        market: str = "future",
        years: int = 2,
        max_concurrent: int = 10,
    ) -> pl.DataFrame:
        df = await self.binance.fetch_history(
            symbol=symbol,
            interval=interval,
            market=market,
            years=years,
            max_concurrent=max_concurrent,
        )

        if df.is_empty():
            return df

        df = df.with_columns(pl.lit(symbol).alias("symbol"), pl.lit(interval).alias("interval"))

        df = self._compute_features(df)

        return df

    @staticmethod
    def _compute_features(df: pl.DataFrame) -> pl.DataFrame:
        c = df["close"].to_numpy().astype(float)
        o = df["open"].to_numpy().astype(float)
        hi = df["high"].to_numpy().astype(float)
        lo = df["low"].to_numpy().astype(float)
        v = df["volume"].to_numpy().astype(float)
        qv = df["quote_volume"].to_numpy().astype(float)
        tbv = df["taker_buy_volume"].to_numpy().astype(float)
        tc = df["trades_count"].to_numpy().astype(float)

        log_ret = np.full(len(c), np.nan)
        log_ret[1:] = np.log(c[1:] / c[:-1])

        prev_c = np.roll(c, 1)
        prev_c[0] = np.nan
        tr = np.maximum(hi - lo, np.maximum(np.abs(hi - prev_c), np.abs(lo - prev_c)))
        tr[0] = np.nan

        avg_trade = np.where(tc > 0, v / tc, np.nan)

        rsi_arr = _rsi(c, 14)
        macd_line, signal_line, histogram = _macd(c)

        out = df.with_columns(
            pl.Series("log_ret", log_ret),
            pl.Series("tr", tr),
            pl.Series("rsi_14", rsi_arr),
            pl.Series("macd", macd_line),
            pl.Series("macd_signal", signal_line),
            pl.Series("macd_hist", histogram),
            pl.Series("obv", _obv(c, v)),
            pl.Series("returns_kurt_20", _rolling_kurt(log_ret, 20)),
            pl.Series("volume_trend_20", _rolling_slope(v, 20)),
            pl.Series("avg_trade_size", avg_trade),
        )

        out = out.with_columns(
            [
                pl.col("log_ret").alias("ret_1b"),
                pl.when(pl.col("open") > 0).then(pl.col("close") / pl.col("open") - 1).otherwise(np.nan).alias(
                    "ret_open_to_close"
                ),
                pl.col("log_ret").shift(2).alias("ret_3b"),
                pl.col("log_ret").shift(4).alias("ret_5b"),
                pl.col("log_ret").shift(9).alias("ret_10b"),
                pl.col("log_ret").shift(19).alias("ret_20b"),
                pl.col("log_ret").shift(59).alias("ret_60b"),
                pl.when(pl.col("close") > 0)
                .then((pl.col("high") - pl.col("low")) / pl.col("close"))
                .otherwise(np.nan)
                .alias("hl_range"),
                pl.when(pl.col("close") > 0)
                .then((pl.col("close") - pl.col("open")).abs() / pl.col("close"))
                .otherwise(np.nan)
                .alias("body_range"),
            ]
        )

        out = out.with_columns(
            [
                pl.col("close").rolling_mean(20, min_periods=20).alias("sma20"),
                pl.col("close").rolling_mean(50, min_periods=50).alias("sma50"),
                pl.col("close").rolling_mean(200, min_periods=200).alias("sma200"),
                pl.col("close").rolling_std(20, min_periods=20).alias("bb_std"),
                pl.col("close").rolling_std(20, min_periods=20).alias("std_20"),
                pl.col("close").rolling_std(50, min_periods=50).alias("std_50"),
                pl.col("close").rolling_std(200, min_periods=200).alias("std_200"),
                pl.col("close").ewm_mean(span=9, adjust=False).alias("ema9"),
                pl.col("close").ewm_mean(span=21, adjust=False).alias("ema21"),
                pl.col("close").ewm_mean(span=50, adjust=False).alias("ema50"),
                pl.col("volume").rolling_mean(20, min_periods=20).alias("volume_sma_20"),
                pl.col("volume").rolling_mean(60, min_periods=60).alias("volume_sma_60"),
                pl.col("volume").rolling_std(20, min_periods=20).alias("volume_std_20"),
                pl.col("volume").rolling_std(60, min_periods=60).alias("volume_std_60"),
                pl.col("high").rolling_max(20, min_periods=20).alias("rolling_high_20"),
                pl.col("low").rolling_min(20, min_periods=20).alias("rolling_low_20"),
                pl.col("log_ret").rolling_std(20, min_periods=20).alias("vol_20"),
                pl.col("log_ret").rolling_std(60, min_periods=60).alias("vol_60"),
                pl.col("log_ret").rolling_skew(20, bias=False, min_samples=20).alias("returns_skew_20"),
                pl.col("log_ret").rolling_mean(20, min_periods=20).alias("return_mean_20"),
                pl.col("log_ret").rolling_std(20, min_periods=20).alias("return_std_20"),
                pl.col("log_ret").rolling_mean(60, min_periods=60).alias("return_mean_60"),
                pl.col("log_ret").rolling_std(60, min_periods=60).alias("return_std_60"),
                pl.col("macd_hist").rolling_mean(20, min_periods=20).alias("macd_hist_mean_20"),
                pl.col("macd_hist").rolling_std(20, min_periods=20).alias("macd_hist_std_20"),
                pl.col("tr").rolling_mean(14, min_periods=14).alias("atr14"),
                pl.col("close").cum_max().alias("peak"),
                pl.col("trades_count").cast(pl.Float64).rolling_mean(20, min_periods=20).alias("tc_mean_20"),
                pl.col("trades_count").cast(pl.Float64).rolling_std(20, min_periods=20).alias("tc_std_20"),
            ]
        )

        out = out.with_columns(
            [
                pl.when(pl.col("sma20") > 0)
                .then((pl.col("close") - pl.col("sma20")) / pl.col("sma20"))
                .otherwise(np.nan)
                .alias("dist_sma_20"),
                pl.when(pl.col("sma50") > 0)
                .then((pl.col("close") - pl.col("sma50")) / pl.col("sma50"))
                .otherwise(np.nan)
                .alias("dist_sma_50"),
                pl.when(pl.col("sma200") > 0)
                .then((pl.col("close") - pl.col("sma200")) / pl.col("sma200"))
                .otherwise(np.nan)
                .alias("dist_sma_200"),
                pl.when(pl.col("ema21") > 0)
                .then((pl.col("ema9") - pl.col("ema21")) / pl.col("ema21"))
                .otherwise(np.nan)
                .alias("ema_diff_9_21"),
                pl.when(pl.col("ema50") > 0)
                .then((pl.col("ema21") - pl.col("ema50")) / pl.col("ema50"))
                .otherwise(np.nan)
                .alias("ema_diff_21_50"),
                pl.when(pl.col("close") > 0)
                .then(pl.col("atr14") / pl.col("close"))
                .otherwise(np.nan)
                .alias("atr_14_norm"),
                pl.when(pl.col("volume_sma_20") > 0)
                .then(pl.col("volume") / pl.col("volume_sma_20"))
                .otherwise(np.nan)
                .alias("volume_rel_20"),
                pl.when(pl.col("volume") > 0)
                .then(pl.col("taker_buy_volume") / pl.col("volume"))
                .otherwise(np.nan)
                .alias("taker_buy_vol_ratio"),
                (pl.col("sma20") + 2 * pl.col("bb_std")).alias("bb_upper"),
                (pl.col("sma20") - 2 * pl.col("bb_std")).alias("bb_lower"),
                pl.when(pl.col("peak") > 0)
                .then((pl.col("close") - pl.col("peak")) / pl.col("peak"))
                .otherwise(np.nan)
                .alias("drawdown"),
                pl.when(pl.col("quote_volume") > 0)
                .then(pl.col("log_ret").abs() / pl.col("quote_volume"))
                .otherwise(np.nan)
                .alias("amihud_illiquidity"),
                pl.when(pl.col("return_std_20") > 0)
                .then((pl.col("log_ret") - pl.col("return_mean_20")) / pl.col("return_std_20"))
                .otherwise(np.nan)
                .alias("return_zscore_20"),
                pl.when(pl.col("return_std_60") > 0)
                .then((pl.col("log_ret") - pl.col("return_mean_60")) / pl.col("return_std_60"))
                .otherwise(np.nan)
                .alias("return_zscore_60"),
                pl.when(pl.col("std_20") > 0)
                .then((pl.col("close") - pl.col("sma20")) / pl.col("std_20"))
                .otherwise(np.nan)
                .alias("price_zscore_20"),
                pl.when(pl.col("std_50") > 0)
                .then((pl.col("close") - pl.col("sma50")) / pl.col("std_50"))
                .otherwise(np.nan)
                .alias("price_zscore_50"),
                pl.when(pl.col("std_200") > 0)
                .then((pl.col("close") - pl.col("sma200")) / pl.col("std_200"))
                .otherwise(np.nan)
                .alias("price_zscore_200"),
                pl.when(pl.col("rolling_high_20") > 0)
                .then((pl.col("rolling_high_20") - pl.col("high")) / pl.col("rolling_high_20"))
                .otherwise(np.nan)
                .alias("high_distance_20"),
                pl.when(pl.col("rolling_low_20") > 0)
                .then((pl.col("low") - pl.col("rolling_low_20")) / pl.col("rolling_low_20"))
                .otherwise(np.nan)
                .alias("low_distance_20"),
                pl.when(pl.col("volume_std_20") > 0)
                .then((pl.col("volume") - pl.col("volume_sma_20")) / pl.col("volume_std_20"))
                .otherwise(np.nan)
                .alias("volume_zscore_20"),
                pl.when(pl.col("volume_std_60") > 0)
                .then((pl.col("volume") - pl.col("volume_sma_60")) / pl.col("volume_std_60"))
                .otherwise(np.nan)
                .alias("volume_zscore_60"),
                pl.when(pl.col("volume").shift(1) > 0)
                .then(pl.col("volume") / pl.col("volume").shift(1) - 1)
                .otherwise(np.nan)
                .alias("volume_change_1"),
                pl.when(pl.col("volume").shift(5) > 0)
                .then(pl.col("volume") / pl.col("volume").shift(5) - 1)
                .otherwise(np.nan)
                .alias("volume_change_5"),
                pl.when(pl.col("volume_sma_60") > 0)
                .then(pl.col("volume_sma_20") / pl.col("volume_sma_60"))
                .otherwise(np.nan)
                .alias("vol_ratio_20_60"),
                pl.when(pl.col("vol_20").shift(1) > 0)
                .then(pl.col("vol_20") / pl.col("vol_20").shift(1) - 1)
                .otherwise(np.nan)
                .alias("vol_change_1"),
                pl.when(pl.col("vol_20").shift(5) > 0)
                .then(pl.col("vol_20") / pl.col("vol_20").shift(5) - 1)
                .otherwise(np.nan)
                .alias("vol_change_5"),
                pl.when(pl.col("atr14").shift(14) > 0)
                .then(pl.col("atr14") / pl.col("atr14").shift(14) - 1)
                .otherwise(np.nan)
                .alias("atr_ratio"),
                pl.when(pl.col("macd_hist_std_20") > 0)
                .then(
                    (pl.col("macd_hist") - pl.col("macd_hist_mean_20")) / pl.col("macd_hist_std_20")
                )
                .otherwise(np.nan)
                .alias("macd_hist_zscore_20"),
            ]
        )

        out = out.with_columns(
            [
                (pl.max_horizontal("open", "close")).alias("_real_body_high"),
                (pl.min_horizontal("open", "close")).alias("_real_body_low"),
            ]
        )

        out = out.with_columns(
            [
                (pl.col("high") - pl.col("_real_body_high")).alias("upper_wick"),
                (pl.col("_real_body_low") - pl.col("low")).alias("lower_wick"),
            ]
        )

        out = out.with_columns(
            [
                pl.when((pl.col("high") - pl.col("low")) > 0)
                .then(pl.col("upper_wick") / (pl.col("high") - pl.col("low")))
                .otherwise(np.nan)
                .alias("upper_wick_ratio"),
                pl.when((pl.col("high") - pl.col("low")) > 0)
                .then(pl.col("lower_wick") / (pl.col("high") - pl.col("low")))
                .otherwise(np.nan)
                .alias("lower_wick_ratio"),
                pl.when((pl.col("high") - pl.col("low")) > 0)
                .then((pl.col("close") - pl.col("open")).abs() / (pl.col("high") - pl.col("low")))
                .otherwise(np.nan)
                .alias("body_to_range"),
                pl.when(pl.col("sma20") > 0)
                .then((pl.col("bb_upper") - pl.col("bb_lower")) / pl.col("sma20"))
                .otherwise(np.nan)
                .alias("bb_width"),
                pl.when((pl.col("bb_upper") - pl.col("bb_lower")) > 0)
                .then((pl.col("close") - pl.col("bb_lower")) / (pl.col("bb_upper") - pl.col("bb_lower")))
                .otherwise(np.nan)
                .alias("bb_pct"),
            ]
        )

        out = out.with_columns(
            [
                (pl.col("rsi_14") - pl.col("rsi_14").shift(1)).alias("rsi_change_1"),
                (pl.col("rsi_14") - pl.col("rsi_14").shift(5)).alias("rsi_change_5"),
                (pl.col("macd_hist") - pl.col("macd_hist").shift(1)).alias("macd_hist_change_1"),
                (pl.col("macd_hist") - pl.col("macd_hist").shift(5)).alias("macd_hist_change_5"),
                pl.col("bb_width").rolling_mean(20, min_periods=20).alias("bb_width_mean_20"),
                pl.col("bb_width").rolling_std(20, min_periods=20).alias("bb_width_std_20"),
                (pl.col("bb_width") - pl.col("bb_width").shift(1)).alias("bb_width_change"),
                (pl.col("bb_pct") - pl.col("bb_pct").shift(1)).alias("bb_pct_change"),
                (pl.col("taker_buy_vol_ratio") - pl.col("taker_buy_vol_ratio").shift(1)).alias(
                    "buy_pressure_change"
                ),
                pl.when(pl.col("trades_count").cast(pl.Float64).shift(1) > 0)
                .then(
                    pl.col("trades_count").cast(pl.Float64) / pl.col("trades_count").cast(pl.Float64).shift(1) - 1
                )
                .otherwise(np.nan)
                .alias("trade_count_change"),
                pl.when(pl.col("tc_std_20") > 0)
                .then(
                    (pl.col("trades_count").cast(pl.Float64) - pl.col("tc_mean_20")) / pl.col("tc_std_20")
                )
                .otherwise(np.nan)
                .alias("trade_count_zscore_20"),
                pl.col("avg_trade_size").rolling_mean(20, min_periods=20).alias("avg_trade_mean_20"),
                pl.col("avg_trade_size").rolling_std(20, min_periods=20).alias("avg_trade_std_20"),
                (pl.col("drawdown") - pl.col("drawdown").shift(1)).alias("drawdown_change"),
            ]
        )

        out = out.with_columns(
            [
                pl.when(pl.col("bb_width_std_20") > 0)
                .then((pl.col("bb_width") - pl.col("bb_width_mean_20")) / pl.col("bb_width_std_20"))
                .otherwise(np.nan)
                .alias("bb_width_zscore_20"),
                pl.when(pl.col("avg_trade_std_20") > 0)
                .then((pl.col("avg_trade_size") - pl.col("avg_trade_mean_20")) / pl.col("avg_trade_std_20"))
                .otherwise(np.nan)
                .alias("avg_trade_size_zscore_20"),
            ]
        )

        peak_arr = out["peak"].to_numpy()
        dd_duration = np.full(len(c), np.nan)
        dd_recovery = np.full(len(c), np.nan)
        trough_since_peak = c[0]
        for i in range(1, len(c)):
            if peak_arr[i] == peak_arr[i - 1]:
                dd_duration[i] = dd_duration[i - 1] + 1 if not np.isnan(dd_duration[i - 1]) else 1
                trough_since_peak = min(trough_since_peak, c[i])
            else:
                dd_duration[i] = 0
                trough_since_peak = c[i]
            peak_val = peak_arr[i]
            if peak_val > trough_since_peak:
                dd_recovery[i] = (c[i] - trough_since_peak) / (peak_val - trough_since_peak)
            else:
                dd_recovery[i] = 1.0

        out = out.with_columns(
            pl.Series("drawdown_duration", dd_duration),
            pl.Series("recovery_from_drawdown", dd_recovery),
        )

        drop_cols = [
            "log_ret",
            "tr",
            "sma20",
            "sma50",
            "sma200",
            "std_20",
            "std_50",
            "std_200",
            "bb_std",
            "ema9",
            "ema21",
            "ema50",
            "volume_sma_60",
            "volume_std_20",
            "volume_std_60",
            "rolling_high_20",
            "rolling_low_20",
            "return_mean_60",
            "return_std_60",
            "macd_hist_mean_20",
            "macd_hist_std_20",
            "atr14",
            "peak",
            "tc_mean_20",
            "tc_std_20",
            "bb_width_mean_20",
            "bb_width_std_20",
            "avg_trade_mean_20",
            "avg_trade_std_20",
            "_real_body_high",
            "_real_body_low",
        ]
        out = out.drop([c for c in drop_cols if c in out.columns])

        return out


def _rsi(closes: np.ndarray, period: int = 14) -> np.ndarray:
    deltas = np.diff(closes, prepend=closes[0])
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)

    avg_gain = np.full(len(closes), np.nan)
    avg_loss = np.full(len(closes), np.nan)

    if len(closes) < period + 1:
        return avg_gain

    avg_gain[period] = np.mean(gains[1 : period + 1])
    avg_loss[period] = np.mean(losses[1 : period + 1])

    for i in range(period + 1, len(closes)):
        avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gains[i]) / period
        avg_loss[i] = (avg_loss[i - 1] * (period - 1) + losses[i]) / period

    rs = np.where(avg_loss > 0, avg_gain / avg_loss, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def _macd(
    closes: np.ndarray,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    cs = pl.Series(closes, dtype=pl.Float64)
    ema_fast = cs.ewm_mean(span=fast, adjust=False)
    ema_slow = cs.ewm_mean(span=slow, adjust=False)
    macd_line = (ema_fast - ema_slow).to_numpy()
    signal_line = pl.Series(macd_line, dtype=pl.Float64).ewm_mean(span=signal, adjust=False).to_numpy()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def _obv(closes: np.ndarray, volumes: np.ndarray) -> np.ndarray:
    direction = np.sign(np.diff(closes, prepend=closes[0]))
    obv = np.cumsum(direction * volumes)
    return obv


def _rolling_slope(series: np.ndarray, window: int) -> np.ndarray:
    x = np.arange(window, dtype=float)
    x_mean = x.mean()
    x_var = ((x - x_mean) ** 2).sum()
    vals = np.asarray(series, dtype=float)
    result = np.full(len(vals), np.nan)
    for i in range(window - 1, len(vals)):
        y = vals[i - window + 1 : i + 1]
        if np.any(np.isnan(y)):
            continue
        y_mean = y.mean()
        if x_var == 0:
            result[i] = 0.0
        else:
            result[i] = ((x - x_mean) * (y - y_mean)).sum() / x_var
    return result


def _rolling_kurt(vals: np.ndarray, w: int) -> np.ndarray:
    """Unbiased (Fisher) excess kurtosis matching pandas ``rolling(w).kurt()``."""
    out = np.full(len(vals), np.nan)
    for i in range(w - 1, len(vals)):
        y = vals[i - w + 1 : i + 1]
        if np.any(np.isnan(y)):
            continue
        m = np.mean(y)
        dev = y - m
        s2 = np.sum(dev**2)
        if s2 == 0:
            continue
        m4 = np.sum(dev**4)
        k = (w * (w + 1) * (w - 1)) / ((w - 2) * (w - 3)) * m4 / (s2**2) - (3 * (w - 1) ** 2) / ((w - 2) * (w - 3))
        out[i] = k
    return out


def _to_float(value: object) -> float:
    return float(value)  # type: ignore


def _extract_periods(facts: dict, quarters: int) -> list[dict]:
    seen_periods: set[tuple[int, str]] = set()
    rows: list[dict] = []

    for field, tags in SEC_TAG_MAP.items():
        for tag in tags:
            if tag not in facts:
                continue
            tag_data = facts[tag]
            units = tag_data.get("units", {})
            for unit_type, entries in units.items():
                for entry in entries:
                    fy = entry.get("fy")
                    fp = entry.get("fp")
                    if fy is None or fp is None:
                        continue
                    period_key = (fy, fp)
                    if period_key in seen_periods:
                        continue
                    seen_periods.add(period_key)
                    rows.append(
                        {
                            "fiscal_year": fy,
                            "fiscal_period": fp,
                            "filing_date": entry.get("filed"),
                            "filing_type": entry.get("form"),
                        }
                    )
                break
            if rows:
                break
        if rows:
            break

    rows.sort(key=lambda r: (r["fiscal_year"], r["fiscal_period"]), reverse=True)
    return rows[:quarters]


def _extract_funds_per_period(facts: dict, periods: list[dict], symbol: str) -> list[dict]:
    result_rows: list[dict] = []

    for period in periods:
        period_facts: dict[str, object] = {}
        for field, tags in SEC_TAG_MAP.items():
            period_facts[field] = None
            for tag in tags:
                if tag not in facts:
                    continue
                tag_data = facts[tag]
                units = tag_data.get("units", {})
                for unit_type, entries in units.items():
                    for entry in entries:
                        if entry.get("fy") == period["fiscal_year"] and entry.get("fp") == period["fiscal_period"]:
                            period_facts[field] = entry.get("val")
                            break
                    if period_facts[field] is not None:
                        break
                if period_facts[field] is not None:
                    break

        r = period_facts.get("revenue")
        cor = period_facts.get("cost_of_revenue")
        oi = period_facts.get("operating_income")
        gp = period_facts.get("gross_profit")

        if gp is None and r is not None and cor is not None:
            try:
                period_facts["gross_profit"] = _to_float(r) - _to_float(cor)
            except (TypeError, ValueError):
                pass

        gp = period_facts.get("gross_profit")
        if period_facts.get("operating_expenses") is None and gp is not None and oi is not None:
            try:
                period_facts["operating_expenses"] = _to_float(gp) - _to_float(oi)
            except (TypeError, ValueError):
                pass

        result_rows.append(
            {
                "ticker": symbol,
                "filing_date": period["filing_date"],
                "fiscal_period": period["fiscal_period"],
                "fiscal_year": period["fiscal_year"],
                "filing_type": period["filing_type"],
                **period_facts,
            }
        )

    return result_rows