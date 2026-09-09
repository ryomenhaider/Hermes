import polars as pl


def klines_to_dataframe(all_candles: list) -> pl.DataFrame:
    if not all_candles:
        return pl.DataFrame()

    df = pl.DataFrame(
        all_candles,
        schema=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_volume",
            "trades_count",
            "taker_buy_volume",
            "taker_buy_quote_volume",
            "ignore",
        ],
    )

    for col in [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "quote_volume",
        "taker_buy_volume",
        "taker_buy_quote_volume",
    ]:
        df = df.with_columns(pl.col(col).cast(pl.Float64))

    df = df.with_columns(pl.col("trades_count").cast(pl.Int64))
    df = df.drop("ignore")
    df = df.unique(subset=["open_time"], keep="first")
    df = df.sort("open_time")

    return df


__all__ = ["klines_to_dataframe"]
