import polars as pl


def candles_to_dataframe(all_candles: list) -> pl.DataFrame:
    if not all_candles:
        return pl.DataFrame()

    df = pl.DataFrame(
        all_candles,
        schema=["open_time", "open", "high", "low", "close", "volume"],
    )

    for col in ["open", "high", "low", "close", "volume"]:
        df = df.with_columns(pl.col(col).cast(pl.Float64))

    df = df.unique(subset=["open_time"], keep="first")
    df = df.sort("open_time")

    return df


__all__ = ["candles_to_dataframe"]
