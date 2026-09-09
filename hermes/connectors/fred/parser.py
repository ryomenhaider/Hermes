import polars as pl


def observations_to_dataframe(r: dict, series_id: str) -> pl.DataFrame:
    df = pl.DataFrame(r["observations"]).drop(["realtime_start", "realtime_end"])
    df = df.with_columns(pl.lit(series_id).alias("series_id"))
    df = df.with_columns(pl.lit(r["units"]).alias("unit"))
    df = df.sort("date", descending=True)
    return df


__all__ = ["observations_to_dataframe"]
