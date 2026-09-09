import polars as pl


def history_to_dataframe(df: pd.DataFrame) -> pl.DataFrame:
    if df is None or df.empty:
        return pl.DataFrame()

    df = df.reset_index()
    rename = {}
    for col in df.columns:
        lc = col.lower()
        if lc == "date" or lc == "datetime":
            rename[col] = "timestamp_ms"
        elif lc in ("open", "high", "low", "close", "volume"):
            rename[col] = lc
        elif lc == "adj close":
            rename[col] = "adj_close"
    df = df.rename(columns=rename)

    if "timestamp_ms" in df.columns:
        df["timestamp_ms"] = pd.to_datetime(df["timestamp_ms"]).astype("int64") // 10**6

    keep = [c for c in ["timestamp_ms", "open", "high", "low", "close", "volume", "adj_close"] if c in df.columns]
    df = df[keep].copy()

    for col in ["open", "high", "low", "close", "volume"]:
        if col in df.columns:
            df[col] = df[col].astype(float)

    df = df.drop_duplicates(subset=["timestamp_ms"], keep="first")
    df = df.sort_values("timestamp_ms").reset_index(drop=True)

    return pl.from_pandas(df)


__all__ = ["history_to_dataframe"]
