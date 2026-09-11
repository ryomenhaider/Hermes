import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import polars as pl
import polars.selectors as cs

from hermes.core.errors import HermesError
from hermes.core.metadata import ColumnMetadata, InspectReport, MetaData, QualityInfo
from hermes.core.result import Result

logger = logging.getLogger(__name__)


def parse(data: object, **kwargs: object) -> Result:
    raise NotImplementedError()


def normalize(data: object, **kwargs: object) -> Result:
    raise NotImplementedError()


def validate(
    data: object,
    contract: object | None = None
) -> Result:

    raise NotImplementedError()


def transform(
    data: object,
    fn: object | None = None,
    **kwargs: object
) -> Result:

    raise NotImplementedError()


def inspect(data: pl.DataFrame) -> InspectReport:
    if data is None:
        raise HermesError("No data provided to inspect()")

    if isinstance(data, pl.LazyFrame):
        data = data.collect()
    elif not isinstance(data, pl.DataFrame):
        data = pl.DataFrame(data)

    columns = [(col, str(data.schema[col])) for col in data.columns]

    return InspectReport(
        name="dataset",
        row_count=data.height,
        column_count=data.width,
        columns=columns,
        sample=data.head(5).to_dicts(),
    )


def get_time_cols(data: pl.DataFrame) -> list[str] | None:
    time_cols = list(data.select(cs.temporal()).columns)
    if not time_cols:
        logger.info("No temporal columns found")
        return None
    return time_cols


def get_freqs(data: pl.DataFrame) -> list[str] | None:
    time_cols = get_time_cols(data)
    if not time_cols:
        logger.info('No frequency found')
        return None

    cols = []
    for col in time_cols:
        freq = data[col].diff().mode().first()
        cols.append(str(freq))

    return cols


def date_ranges(
    data: pl.DataFrame | pl.LazyFrame
) -> list[dict[str, tuple[Any, Any]]] | None:

    if isinstance(data, pl.LazyFrame):
        data = data.collect()
    time_cols = get_time_cols(data)

    if not time_cols:
        logger.info('no date found')
        return None

    bounds = []
    for col in time_cols:
        bound = data.select(min=pl.col(col).min(), max=pl.col(col).max())
        bounds.append({col: (bound["min"][0], bound["max"][0])})

    return bounds


def anomaly_count(data: pl.DataFrame | pl.LazyFrame, threshold: float = 1.5) -> dict[str, int]:
    if isinstance(data, pl.LazyFrame):
        data = data.collect()

    num_cols = data.select(cs.numeric()).columns
    if not num_cols:
        return {}

    anomaly_exprs = []
    for col in num_cols:
        q1 = pl.col(col).quantile(0.25)
        q3 = pl.col(col).quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - (threshold * iqr)
        upper_bound = q3 + (threshold * iqr)

        is_anomaly = (pl.col(col) < lower_bound) | (pl.col(col) > upper_bound)
        anomaly_exprs.append(is_anomaly.sum().alias(col))

    anomaly_data = data.select(anomaly_exprs)
    return anomaly_data.row(0, named=True)


def profile(data: object | None = None, path: Path | None = None, source: str | None = None) -> MetaData:
    if data is not None:
        if isinstance(data, pl.LazyFrame):
            data = data.collect()
        elif not isinstance(data, pl.DataFrame):
            data = pl.DataFrame(data)
    elif path:
        path = Path(path)
        if path.suffix.lower() == ".csv":
            data = pl.read_csv(path)
        elif path.suffix.lower() == ".parquet":
            data = pl.read_parquet(path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
    else:
        raise ValueError("Either data or path must be provided")

    stats_df = data.select([
        pl.all().null_count().name.suffix("_null_count"),
        pl.all().n_unique().name.suffix("_unique_count"),
        cs.numeric().min().name.suffix("_min"),
        cs.numeric().max().name.suffix("_max"),
        cs.numeric().mean().name.suffix("_mean"),
        cs.numeric().median().name.suffix("_median"),
        cs.numeric().std().name.suffix("_std"),
    ])
    stats = stats_df.row(0, named=True)

    string_cols = data.select(cs.string()).columns
    top_values_map = {}

    for col in string_cols:
        structs = (
            data.select(pl.col(col).value_counts(sort=True).head(5))
            .to_series()
            .to_list()
        )
        top_values_map[col] = [
            (item[col], item["count"]) for item in structs if item is not None
        ]

    col_metadata = []
    total_rows = len(data)

    for col in data.columns:
        is_numeric = data.schema[col].is_numeric()
        null_count = stats[f"{col}_null_count"]

        col_metadata.append(
            ColumnMetadata(
                name=col,
                dtype=str(data.schema[col]),
                null_count=null_count,
                null_ratio=float(null_count / total_rows) if total_rows > 0 else 0.0,
                unique_count=stats[f"{col}_unique_count"],
                min_value=stats.get(f"{col}_min") if is_numeric else None,
                max_value=stats.get(f"{col}_max") if is_numeric else None,
                mean=stats.get(f"{col}_mean") if is_numeric else None,
                median=stats.get(f"{col}_median") if is_numeric else None,
                std=stats.get(f"{col}_std") if is_numeric else None,
                top_values=top_values_map.get(col, []),
            )
        )

    null_df = data.select(pl.all().is_null().mean())
    completeness_map = null_df.select(pl.all().sub(1.0).abs()).row(0, named=True)

    duplicate_count = int(data.is_duplicated().sum())

    data_quality = QualityInfo(
        completeness=completeness_map,
        duplicate_count=duplicate_count,
        anomaly_count=anomaly_count(data),
    )
    _date_ranges = date_ranges(data)
    _freq = get_freqs(data)

    return MetaData(
        row_count=data.height,
        column_count=data.width,
        columns=col_metadata,
        date_range=_date_ranges[0] if _date_ranges else None,
        frequency=_freq[0] if _freq else None,
        source=source,
        retrieved_at=datetime.now(tz=UTC),
        profiled_at=datetime.now(tz=UTC),
        quality=data_quality,
    )
