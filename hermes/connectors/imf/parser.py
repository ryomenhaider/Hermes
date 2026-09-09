import polars as pl

EMPTY_COLS = ["date", "indicator_id", "country", "value", "source"]


def empty_dataframe() -> pl.DataFrame:
    return pl.DataFrame(schema={c: pl.String for c in EMPTY_COLS})


def parse_sdmx_json(data, country: str, key: str) -> pl.DataFrame:
    """Convert an SDMX-JSON data payload into a canonical polars DataFrame."""
    if not isinstance(data, dict):
        return empty_dataframe()

    data_sets = data.get("dataSets")
    structures = data.get("structures")
    if not data_sets or not structures:
        return empty_dataframe()

    series_map = (data_sets[0] or {}).get("series")
    if not series_map:
        return empty_dataframe()

    observations = next(iter(series_map.values()))["observations"]

    dims = structures[0].get("dimensions", {})

    indicator_id = key
    for dim in dims.get("series") or []:
        if dim.get("id") == "INDICATOR":
            values = dim.get("values") or []
            if values:
                indicator_id = values[0].get("id", key)
            break

    time_values: list[str] = []
    for dim in dims.get("observation") or []:
        if dim.get("id") == "TIME_PERIOD":
            time_values = [str(v.get("id", "")) for v in dim.get("values", [])]
            break

    rows = []
    for obs_key, payload in observations.items():
        try:
            idx = int(obs_key)
        except (TypeError, ValueError):
            continue
        period = time_values[idx] if idx < len(time_values) else str(idx)
        rows.append({"date": period, "value": payload[0]})

    if not rows:
        return empty_dataframe()

    return pl.DataFrame(rows).with_columns(
        pl.lit(country).alias("country"),
        pl.lit(indicator_id).alias("indicator_id"),
        pl.lit("IMF").alias("source"),
    )


__all__ = ["EMPTY_COLS", "empty_dataframe", "parse_sdmx_json"]
