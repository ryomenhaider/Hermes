import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import polars as pl
import polars.selectors as cs
import pyarrow as pa

from hermes.core.dataset import Dataset
from hermes.core.errors import HermesError, ParseError
from hermes.core.metadata import ColumnMetadata, InspectReport, MetaData, QualityInfo
from hermes.normalization.context import NormalizationContext
from hermes.normalization.engine import NormalizationEngine
from hermes.normalization.rule import NormalizationRule
from hermes.parsing.engine import ParserEngine
from hermes.validation.engine import validate as validate_frame
from hermes.validation.result import ValidationResult

logger = logging.getLogger(__name__)


def parse(data: object, format: str | None = None, **kwargs: object) -> Dataset:
    ref = None
    if isinstance(data, Dataset):
        dataset = data
        source = dataset.data if dataset.data is not None else dataset.data_ref
        input_ref = str(dataset.data_ref) if dataset.data_ref else None
    else:
        dataset = None
        source = data
        input_ref = str(data) if isinstance(data, (str, Path)) else None

    df = _frame_or_parse(source, format=format, **kwargs)

    if dataset is not None:
        if source is None:
            dataset.record("parse", input_ref=input_ref, params={"format": format})
            return dataset
        dataset.data = df
        dataset.record("parse", input_ref=input_ref, params={"format": format})
        return dataset

    name = Path(data).stem if isinstance(data, (str, Path)) else "dataset"  # type: ignore[arg-type]
    ds = Dataset(name=name, data=df, data_ref=input_ref)
    ds.record("parse", input_ref=input_ref, params={"format": format})
    return ds


def _frame_or_parse(source: object, format: str | None = None, **kwargs: object):
    if isinstance(source, pl.LazyFrame):
        return source
    if isinstance(source, pl.DataFrame):
        return source
    if isinstance(source, pa.Table):
        return pl.from_arrow(source)
    if isinstance(source, dict) or (
        isinstance(source, (list, tuple)) and source and isinstance(source[0], dict)
    ):
        try:
            return pl.DataFrame(source)
        except Exception as exc:  # noqa: BLE001 - wrap user data into a parse error
            raise ParseError(f"Could not build a frame from {type(source).__name__}: {exc}") from exc
    if isinstance(source, (str, Path)) and format is None:
        scanned = ParserEngine().scan(source)
        if scanned is not None:
            return scanned
    return ParserEngine().parse(source, format=format, **kwargs)


def _rule_labels(rules: list | None) -> list:
    labels = []
    for rule in rules or []:
        describe = getattr(rule, "describe", None)
        labels.append(describe() if callable(describe) else getattr(rule, "name", str(rule)))
    return labels


def normalize(
    data: object,
    rules: list[NormalizationRule] | None = None,
    report: bool = False,
    context: NormalizationContext | None = None,
) -> object:

    engine = NormalizationEngine(rules=rules or [], context=context)
    if isinstance(data, Dataset):
        if report:
            result = engine.normalize_report(data.data)
            data.data = result.data
        else:
            data.data = engine.normalize(data.data)
        data.record("normalize", params={"rules": _rule_labels(rules), "report": report})
        return result if report else data

    if report:
        return engine.normalize_report(data)
    return engine.normalize(data)


def validate(data: object, rules: list | None = None) -> ValidationResult:
    if isinstance(data, Dataset):
        result = validate_frame(data.data, rules=rules)
        data.record(
            "validate",
            params={"rules": _rule_labels(rules), "passed": result.passed, "errors": len(result.errors)},
            version=False,
        )
        return result
    return validate_frame(data, rules=rules)


def transform(data: object, fn: object | None = None, **kwargs: object) -> object:
    if not callable(fn):
        raise ValueError("transform requires a callable fn")

    frame = data.data if isinstance(data, Dataset) else data
    if frame is None:
        raise HermesError("No data to transform")

    transformed = fn(frame, **kwargs)

    if isinstance(data, Dataset):
        data.data = transformed
        data.record("transform", params={"fn": getattr(fn, "__name__", "transform")})
        return data
    return transformed


def inspect(data: pl.DataFrame | pl.LazyFrame) -> InspectReport:
    if data is None:
        raise HermesError("No data provided to inspect()")

    if isinstance(data, pl.LazyFrame):
        schema = data.collect_schema()
        columns = [(col, str(dtype)) for col, dtype in schema.items()]
        row_count = int(data.select(pl.len()).collect(engine='streaming').item())
        sample = data.head(5).collect(engine='streaming').to_dicts()
        return InspectReport(
            name="dataset",
            row_count=row_count,
            column_count=len(columns),
            columns=columns,
            sample=sample,
        )

    if not isinstance(data, pl.DataFrame):
        data = pl.DataFrame(data)

    columns = [(col, str(data.schema[col])) for col in data.columns]

    return InspectReport(
        name="dataset",
        row_count=data.height,
        column_count=data.width,
        columns=columns,
        sample=data.head(5).to_dicts(),
    )


def get_time_cols(data: pl.DataFrame | pl.LazyFrame) -> list[str] | None:
    if isinstance(data, pl.LazyFrame):
        time_cols = [col for col, dtype in data.collect_schema().items() if dtype.is_temporal()]
    else:
        time_cols = list(data.select(cs.temporal()).columns)
    if not time_cols:
        logger.info("No temporal columns found")
        return None
    return time_cols


def get_freqs(data: pl.DataFrame | pl.LazyFrame) -> list[str] | None:
    time_cols = get_time_cols(data)
    if not time_cols:
        logger.info("No frequency found")
        return None

    cols = []
    for col in time_cols:
        if isinstance(data, pl.LazyFrame):
            freq = data.select(pl.col(col).diff().mode().first()).collect(engine='streaming').item()
        else:
            freq = data[col].diff().mode().first()
        cols.append(str(freq))

    return cols


def date_ranges(data: pl.DataFrame | pl.LazyFrame) -> list[dict[str, tuple[Any, Any]]] | None:

    time_cols = get_time_cols(data)

    if not time_cols:
        logger.info("no date found")
        return None

    bounds = []
    for col in time_cols:
        if isinstance(data, pl.LazyFrame):
            bound = data.select(min=pl.col(col).min(), max=pl.col(col).max()).collect(engine='streaming')
        else:
            bound = data.select(min=pl.col(col).min(), max=pl.col(col).max())
        bounds.append({col: (bound["min"][0], bound["max"][0])})

    return bounds


def anomaly_count(data: pl.DataFrame | pl.LazyFrame, threshold: float = 1.5) -> dict[str, int]:
    if isinstance(data, pl.LazyFrame):
        num_cols = [col for col, dtype in data.collect_schema().items() if dtype.is_numeric()]
    else:
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
    if isinstance(anomaly_data, pl.LazyFrame):
        anomaly_data = anomaly_data.collect(engine="streaming")
    return anomaly_data.row(0, named=True)


# Memory guardrails for profile(): exact stats that need full sorts or hashes
# (median, n_unique, top values, duplicates, anomaly quantiles, frequency) are
# only computed on small inputs. min/max/null_count come from the parquet footer
# (instant, zero data read); mean/std come from a bounded streaming scan when the
# uncompressed size fits the budget.
_HEAVY_ROWS = 5_000_000
_SCAN_BUDGET_BYTES = 4 * 1024**3


def _parquet_footer(path: Path) -> dict[str, Any]:
    import pyarrow as pa
    import pyarrow.parquet as pq

    pf = pq.ParquetFile(path)
    md = pf.metadata
    ncols = md.num_columns
    fields = [pf.schema_arrow.field(c) for c in range(ncols)]
    mins = [None] * ncols
    maxs = [None] * ncols
    nulls: list[int | None] = [0] * ncols
    for rg in range(md.num_row_groups):
        rgmd = md.row_group(rg)
        for c in range(ncols):
            stats = rgmd.column(c).statistics
            if stats is None:
                nulls[c] = None
                continue
            if stats.has_min_max:
                if mins[c] is None or stats.min < mins[c]:
                    mins[c] = stats.min
                if maxs[c] is None or stats.max > maxs[c]:
                    maxs[c] = stats.max
            if stats.null_count is not None and nulls[c] is not None:
                nulls[c] += stats.null_count

    def decode(field, value):
        if value is None:
            return None
        if pa.types.is_string(field.type) and isinstance(value, bytes):
            return value.decode(errors="replace")
        try:
            return pa.array([value], type=field.type).as_py()
        except Exception:  # noqa: BLE001 - physical value not representable as logical type
            return value

    cols: dict[str, tuple[Any, Any, int | None]] = {}
    for c in range(ncols):
        cols[fields[c].name] = (decode(fields[c], mins[c]), decode(fields[c], maxs[c]), nulls[c])
    bytes_total = sum(md.row_group(i).total_byte_size for i in range(md.num_row_groups))
    return {"rows": md.num_rows, "bytes": bytes_total, "cols": cols}


def _lazy_from_path(path: Path) -> pl.LazyFrame:
    scan = ParserEngine().scan(path)
    return scan if scan is not None else ParserEngine().parse(path).lazy()


def profile(
    data: pl.DataFrame | pl.LazyFrame | None = None,
    path: Path | None = None,
    source: str | None = None,
) -> MetaData:
    footer = None
    heavy = False
    budget_ok = False

    if path is not None and Path(path).suffix.lower() == ".parquet":
        parquet_path = Path(path)
        footer = _parquet_footer(parquet_path)
        ldf: pl.LazyFrame = pl.scan_parquet(parquet_path, low_memory=True)
        schema = ldf.collect_schema()
        total_rows = int(footer["rows"])
        heavy = total_rows <= _HEAVY_ROWS
        budget_ok = footer["bytes"] <= _SCAN_BUDGET_BYTES
    elif data is not None:
        if isinstance(data, pl.LazyFrame):
            ldf = data
        elif isinstance(data, pl.DataFrame):
            ldf = data.lazy()
        else:
            ldf = pl.DataFrame(data).lazy()
        schema = ldf.collect_schema()
        if isinstance(data, pl.DataFrame):
            total_rows = data.height
        else:
            total_rows = int(ldf.select(pl.len()).collect(engine="streaming").item())
        heavy = isinstance(data, pl.DataFrame) or total_rows <= _HEAVY_ROWS
        budget_ok = True
    elif path:
        ldf = _lazy_from_path(Path(path))
        schema = ldf.collect_schema()
        total_rows = int(ldf.select(pl.len()).collect(engine="streaming").item())
        heavy = total_rows <= _HEAVY_ROWS
        budget_ok = True
    else:
        raise ValueError("Either data or path must be provided")

    # Light stats: min/max/null from the parquet footer, or a single bounded
    # streaming pass over the frame.
    stats: dict[str, dict[str, Any]] = {}
    if footer:
        for col, (lo, hi, nc) in footer["cols"].items():
            stats[col] = {"min": lo, "max": hi, "null_count": nc}
        if budget_ok:
            light = (
                ldf.select(
                    cs.numeric().mean().name.suffix("_mean"),
                    cs.numeric().std().name.suffix("_std"),
                )
                .collect(engine="streaming")
                .row(0, named=True)
            )
            for col, value in light.items():
                stats.setdefault(col[: -len("_mean")] if col.endswith("_mean") else col[: -len("_std")], {})[
                    "mean" if col.endswith("_mean") else "std"
                ] = value
    else:
        if budget_ok:
            light = (
                ldf.select(
                    pl.all().null_count().name.suffix("_null_count"),
                    cs.numeric().min().name.suffix("_min"),
                    cs.numeric().max().name.suffix("_max"),
                    cs.numeric().mean().name.suffix("_mean"),
                    cs.numeric().std().name.suffix("_std"),
                    cs.temporal().min().name.suffix("_min"),
                    cs.temporal().max().name.suffix("_max"),
                )
                .collect(engine="streaming")
                .row(0, named=True)
            )
            for col, value in light.items():
                for suffix in ("_null_count", "_min", "_max", "_mean", "_std"):
                    if col.endswith(suffix):
                        stats.setdefault(col[: -len(suffix)], {})[suffix[1:]] = value
                        break
                else:
                    stats.setdefault(col, {})["value"] = value

    # Heavy stats: exact but not streaming-friendly, gated on size.
    top_values_map: dict[str, list[tuple[Any, Any]]] = {}
    duplicate_count = 0
    anomaly = {}
    frequency = None
    if heavy:
        heavy_stats = (
            ldf.select(
                pl.all().n_unique().name.suffix("_unique_count"),
                cs.numeric().median().name.suffix("_median"),
            )
            .collect(engine="streaming")
            .row(0, named=True)
        )
        for col, value in heavy_stats.items():
            for suffix in ("_unique_count", "_median"):
                if col.endswith(suffix):
                    stats.setdefault(col[: -len(suffix)], {})[suffix[1:]] = value
                    break

        for col, dtype in schema.items():
            if dtype != pl.String:
                continue
            structs = (
                ldf.select(pl.col(col).value_counts(sort=True).head(5))
                .collect(engine="streaming")
                .to_series()
                .to_list()
            )
            top_values_map[col] = [(item[col], item["count"]) for item in structs if item is not None]

        if isinstance(data, pl.DataFrame):
            duplicate_count = int(data.is_duplicated().sum())
        else:
            dup_rows = (
                ldf.group_by(pl.all())
                .agg(pl.len().alias("_n"))
                .filter(pl.col("_n") > 1)
                .select(pl.col("_n").sum())
                .collect(engine="streaming")
                .item()
            )
            duplicate_count = int(dup_rows)
        anomaly = anomaly_count(ldf)
        _freq = get_freqs(ldf)
        frequency = _freq[0] if _freq else None

    col_metadata = []
    for col, dtype in schema.items():
        col_stats = stats.get(col, {})
        is_numeric = dtype.is_numeric()
        null_count = col_stats.get("null_count", 0) or 0
        col_metadata.append(
            ColumnMetadata(
                name=col,
                dtype=str(dtype),
                null_count=null_count,
                null_ratio=float(null_count / total_rows) if total_rows > 0 else 0.0,
                unique_count=int(col_stats.get("unique_count", 0) or 0),
                min_value=col_stats.get("min") if (is_numeric or dtype.is_temporal() or footer) else None,
                max_value=col_stats.get("max") if (is_numeric or dtype.is_temporal() or footer) else None,
                mean=col_stats.get("mean") if is_numeric else None,
                median=col_stats.get("median") if is_numeric else None,
                std=col_stats.get("std") if is_numeric else None,
                top_values=top_values_map.get(col, []),
            )
        )

    if footer:
        completeness = {
            col: 1.0 - (nulls / total_rows) if total_rows and nulls is not None else 0.0
            for col, (_, _, nulls) in footer["cols"].items()
        }
    else:
        null_df = ldf.select(pl.all().is_null().mean()).collect(engine="streaming")
        completeness = null_df.select(pl.all().sub(1.0).abs()).row(0, named=True)

    date_range = None
    candidates = {col: (v.get("min"), v.get("max")) for col, v in stats.items()}
    temporal_ranges = {col: v for col, v in candidates.items() if schema[col].is_temporal() and None not in v}
    date_range = temporal_ranges or None

    return MetaData(
        row_count=total_rows,
        column_count=len(schema),
        columns=col_metadata,
        date_range=date_range,
        frequency=frequency,
        source=source,
        retrieved_at=datetime.now(tz=UTC),
        profiled_at=datetime.now(tz=UTC),
        quality=QualityInfo(completeness=completeness, duplicate_count=duplicate_count, anomaly_count=anomaly),
        deep_stats=heavy,
    )
