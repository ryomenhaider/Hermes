try:
    import polars as pl
except ImportError:
    print("This Module Need Polars and PyArrow Installed, use pip/uv install/add hermes-plt[data] ")


def normalize_klines(df: pl.DataFrame) -> pl.DataFrame:
    return df


__all__ = ["normalize_klines"]
