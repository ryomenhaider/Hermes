import logging
from datetime import UTC, datetime
from typing import Any
from pathlib import Path

import polars as pl
import polars.selectors as cs

from hermes.core.metadata import ColumnMetadata, MetaData, QualityInfo, InspectReport
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
    cols = list(data.columns)
    col_data = []
    for col in cols:
        col_data.append(
            {f'{col}', f'{data[col].dtype}'}
        )
        
    return InspectReport(
        row_count=data.height,
        column_count=data.width,
        columns=col_data,

    )


def get_time_cols(data: pl.DataFrame) -> list[str]:
    time_cols = list(data.select(cs.temporal()).columns)
    if not time_cols:
        logger.error("No Temporal Column Found")
        return None
    return time_cols


def get_freqs(data: pl.DataFrame) -> list[str]:
    time_cols = get_time_cols(data)
    if not time_cols:
        logger.error('No frequency found')
        return None
        
    cols = []
    for col in time_cols:
        freq = data[col].diff().mode().first()
        cols.append(str(freq))

    return cols


def date_ranges(
    data: pl.DataFrame | pl.LazyFrame
) -> list[dict[str, tuple[Any, Any]]]:

    if isinstance(data, pl.LazyFrame):
        data = data.collect()
    time_cols = get_time_cols(data)
    
    if not time_cols:
        logger.error('no date found')
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
        cs.numeric().min().cast(pl.Int64).name.suffix("_min"),
        cs.numeric().max().cast(pl.Int64).name.suffix("_max"),
        cs.numeric().mean().name.suffix("_mean"),
        cs.numeric().median().name.suffix("_median"),
        cs.numeric().std().name.suffix("_std"),
    ])
    stats = stats_df.row(0, named=True)

    string_cols = data.select(cs.string()).columns
    top_values_map = {}
    
    if string_cols:
        top_df = data.select([
            pl.col(c).value_counts(sort=True).head(5).name.suffix("_struct") 
            for c in string_cols
        ])
        
        for c in string_cols:
            struct_list = top_df.get_column(f"{c}_struct").to_list()
            top_values_map[c] = [
                (item[c], item["count"]) for item in struct_list if item is not None
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
        date_range=_date_ranges,
        frequency=_freq,
        source=source,
        retrieved_at=datetime.now(tz=UTC),
        quality=data_quality,
    )