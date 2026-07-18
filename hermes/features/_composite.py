"""Composite index calculations: rolling stats, trends, classifications."""

import pandas as pd
import numpy as np


def yoy_growth(series: pd.Series) -> pd.Series:
    return series.pct_change(periods=4) * 100 if len(series) >= 5 else pd.Series(dtype=float)


def qoq_growth(series: pd.Series) -> pd.Series:
    return series.pct_change() * 100 if len(series) >= 2 else pd.Series(dtype=float)


def rolling_volatility(series: pd.Series, window: int = 12) -> float:
    s = series.dropna().tail(window + 1)
    if len(s) < 2:
        return 0.0
    return float(s.pct_change().std() * 100)


def max_drawdown(series: pd.Series) -> float:
    s = series.dropna()
    if len(s) < 2:
        return 0.0
    rolling_max = s.expanding().max()
    dd = (s - rolling_max) / rolling_max
    return float(dd.min())


def classify_trend(recent: float, prior: float) -> str:
    if pd.isna(recent) or pd.isna(prior):
        return "stable"
    if recent == 0 and prior == 0:
        return "stable"
    if prior == 0:
        pct = 100.0 if recent > 0 else -100.0
    else:
        pct = ((recent - prior) / abs(prior)) * 100
    if pct > 20:
        return "escalating"
    if pct < -20:
        return "de-escalating"
    return "stable"


def goldstein_to_violence(avg_tone: float) -> float:
    if pd.isna(avg_tone):
        return 0.5
    return max(0.0, min(1.0, (avg_tone + 10) / 20))


def categorize_regime(democracy_index: float) -> str:
    if pd.isna(democracy_index):
        return "unknown"
    if democracy_index >= 0.7:
        return "democracy"
    if democracy_index >= 0.4:
        return "hybrid"
    return "autocracy"


def normalize_0_1(value: float, min_val: float, max_val: float) -> float:
    if pd.isna(value):
        return 0.5
    return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))
