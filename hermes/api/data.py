import polars as pl
import polars.selectors as cs
from typing import Any
import logging

from hermes.core.result import Result
from hermes.core.metadata import MetaData, ColumnMetadata, QualityInfo

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

def time_col(data: pl.DataFrame):
    time_cols = list(data.select(cs.temporal()).columns)
    if not time_cols:
        raise ValueError('No Temporal Column Found')
    return time_cols

def get_freqs(data: pl.DataFrame) -> str:
    time_cols = time_col(data)

    cols = []
    for col in time_cols:
        freq_df = pl.select(
            freq=pl.col(col).diff().mode().first()
        )
        cols.append(freq_df)

    return cols

def date_ranges(df: pl.DataFrame | pl.LazyFrame) -> list[dict[str, tuple[Any, Any]]]:
    time_col = time_col(df)
    
    bounds = []
    for col in time_col:
        bound = df.select(
            min=pl.col(time_col).min(),
            max=pl.col(time_col).max()
        )
        bounds.append({
                f'{col}': (bound['min'][0], bound['max'][0])
            })
        
    return bounds

def anomaly_count(df: pl.DataFrame | pl.LazyFrame, threshold: float = 1.5) -> dict[str, int]:
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
    if isinstance(df, pl.LazyFrame):
        anomaly_df = anomaly_df.collect()
        
    return anomaly_df.row(0, named=True)

def profile(data: object):
    if not isinstance(data, pl.DataFrame):
        data = pl.DataFrame(data)
    
    col_metadata = []
    
    for col in list(data.columns):
        col_data = data[col]
        
        string_cols = pl.select(cs.string()).columns
        
        if not string_cols:
            logger.warning(f'The Data doesnt Have any string cols, not top values will be shown') 

        
        top_values = {}

        for _col in string_cols:
            top_df = (
                df[_col]
                .value_counts()
                .sort(by="count", descending=True)
                .head(top_n)
            )
            top_values[col] = list(top_df.iter_rows())

        col_metadata.append(
            ColumnMetadata(
                name=f'{col}',
                dtype=f'{col_data.dtype}',
                null_count=f'{col_data.null_count()}',
                null_ratio=f'{col_data.null_count() / len(data)}',
                unique_count=f'{col_data.unique_counts()}',
                min_value=f'{col_data.min()}',
                max_value=f'{col_data.max()}',
                mean=f'{col_data.mean()}',
                median=f'{col_data.median()}',
                std=f'{col_data.std()}',
                top_values=top_values
            )
        )

    completeness_data = data.select(
        1.0 - pl.all().is_null().mean()
    )
    
    duplicated_ = data.select(
        total_dup=pl.all().is_first_distinct().is_not().sum()
    )

    data_quality = QualityInfo(
        completeness=completeness_data.row(0, named=True),
        duplicate_count=duplicated_.item(),
        anomaly_count=anomaly_count(data)
    )
    freq = get_freqs(data)[0]
    date_range = date_ranges(data)[0]

    return MetaData(
        row_count= data.height,
        column_count=data.width,
        columns=col_metadata,
        date_range=date_range,
        frequency=freq,
        source='',
        retrieved_at='',
        quality=data_quality
    )