import logging

import numpy as np
import polars as pl

logger = logging.getLogger(__name__)


def check_empty(mode, data, country="unknown"):
    if isinstance(data, pl.DataFrame) and data.is_empty():
        logger.warning(f"No Data for {country}")
        return empty_result(mode)

    if isinstance(data, pl.DataFrame) and "value" in data.columns:
        data = data.filter(pl.col("value").is_not_null())

    if isinstance(data, pl.DataFrame) and data.is_empty():
        logger.warning(f"No valid data for {country}")
        return empty_result(mode)

    return data


def empty_result(mode: str):
    return np.nan if mode == "F" else pl.Series(dtype=pl.Float64)


def adjust_year_range(df, year_col, start_year, end_year, fill_method="null", fill_value=0):
    full_years = pl.DataFrame({year_col: range(start_year, end_year + 1)})

    df_filtered = df.filter(
        (pl.col(year_col) >= start_year) & (pl.col(year_col) <= end_year)
    )

    adjusted_df = full_years.join(df_filtered, on=year_col, how="left")

    value_cols = [c for c in adjusted_df.columns if c != year_col]

    if fill_method == "value":
        adjusted_df = adjusted_df.with_columns(
            [pl.col(c).fill_null(fill_value) for c in value_cols]
        )
    elif fill_method == "ffill":
        adjusted_df = adjusted_df.with_columns(
            [pl.col(c).forward_fill().backward_fill() for c in value_cols]
        )
    elif fill_method == "bfill":
        adjusted_df = adjusted_df.with_columns(
            [pl.col(c).backward_fill().forward_fill() for c in value_cols]
        )
    elif fill_method == "linear":
        adjusted_df = adjusted_df.with_columns(
            [pl.col(c).interpolate().backward_fill().forward_fill() for c in value_cols]
        )

    return adjusted_df


__all__ = ["check_empty", "empty_result", "adjust_year_range"]