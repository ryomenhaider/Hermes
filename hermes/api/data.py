import logging
from datetime import UTC, datetime
from typing import Any

import polars as pl
import polars.selectors as cs

from hermes.core.metadata import ColumnMetadata, MetaData, QualityInfo
from hermes.core.result import Result

logger = logging.getLogger(__name__)


def parse(data: object, **kwargs: object) -> Result:
    raise NotImplementedError()


def normalize(data: object, **kwargs: object) -> Result:
    raise NotImplementedError()


def validate(data: object, contract: object | None = None) -> Result:
    raise NotImplementedError()


def transform(data: object, fn: object | None = None, **kwargs: object) -> Result:
    raise NotImplementedError()


def inspect(data: object) -> Result:
    raise NotImplementedError()


def get_time_cols(data: pl.DataFrame) -> list[str]:
    time_cols = list(data.select(cs.temporal()).columns)
    if not time_cols:
        raise ValueError("No Temporal Column Found")
    return time_cols


def get_freqs(data: pl.DataFrame) -> list[str]:
    time_cols = get_time_cols(data)

    cols = []
    for col in time_cols:
        freq = data[col].diff().mode().first()
        cols.append(str(freq))

    return cols


def date_ranges(df: pl.DataFrame | pl.LazyFrame) -> list[dict[str, tuple[Any, Any]]]:
    if isinstance(df, pl.LazyFrame):
        df = df.collect()
    time_cols = get_time_cols(df)

    bounds = []
    for col in time_cols:
        bound = df.select(min=pl.col(col).min(), max=pl.col(col).max())
        bounds.append({col: (bound["min"][0], bound["max"][0])})

    return bounds


def anomaly_count(df: pl.DataFrame | pl.LazyFrame, threshold: float = 1.5) -> dict[str, int]:
    if isinstance(df, pl.LazyFrame):
        df = df.collect()

    num_cols = df.select(cs.numeric()).columns
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

    anomaly_df = df.select(anomaly_exprs)
    return anomaly_df.row(0, named=True)


def profile(data: object, top_n: int = 10) -> MetaData:
    if isinstance(data, pl.DataFrame):
        df = data
    elif isinstance(data, pl.LazyFrame):
        df = data.collect()
    else:
        df = pl.DataFrame(data)  # type: ignore[arg-type]

    col_metadata = []

    string_cols = df.select(cs.string()).columns

    if not string_cols:
        logger.warning("The Data doesnt Have any string cols, not top values will be shown")

    for col in list(df.columns):
        col_data = df[col]

        top_values: list[tuple[Any, Any]] = []

        if col in string_cols:
            top_df = df[col].value_counts().sort(by="count", descending=True).head(top_n)
            top_values = list(top_df.iter_rows())

        col_metadata.append(
            ColumnMetadata(
                name=col,
                dtype=str(col_data.dtype),
                null_count=col_data.null_count(),
                null_ratio=col_data.null_count() / len(df),
                unique_count=col_data.n_unique(),
                min_value=col_data.min(),
                max_value=col_data.max(),
                mean=float(col_data.mean() or 0.0),  # type: ignore[arg-type]
                median=float(col_data.median() or 0.0),  # type: ignore[arg-type]
                std=float(col_data.std() or 0.0),  # type: ignore[arg-type]
                top_values=top_values,
            )
        )

    completeness_data = df.select(1.0 - pl.all().is_null().mean())

    duplicated_ = df.select(total_dup=pl.all().is_first_distinct().not_().sum())

    data_quality = QualityInfo(
        completeness=completeness_data.row(0, named=True),
        duplicate_count=duplicated_.item(),
        anomaly_count=anomaly_count(df),
    )
    freq = get_freqs(df)[0]
    date_range = date_ranges(df)[0]

    return MetaData(
        row_count=df.height,
        column_count=df.width,
        columns=col_metadata,
        date_range=date_range,
        frequency=freq,
        source="",
        retrieved_at=datetime.now(tz=UTC),
        quality=data_quality,
    )
