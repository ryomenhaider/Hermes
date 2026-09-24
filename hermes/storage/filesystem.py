from __future__ import annotations

import json
import os
import re
import shutil
import uuid
from dataclasses import asdict, fields, is_dataclass
from datetime import UTC, datetime
from pathlib import Path
from types import UnionType
from typing import Any, Union, cast, get_args, get_origin, get_type_hints

import polars as pl

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError:
    pa = None
    pq = None

from hermes.core.config import get_config
from hermes.core.dataset import Dataset
from hermes.core.errors import StorageError
from hermes.core.lineage import Lineage
from hermes.core.metadata import MetaData
from hermes.core.provenance import Provenance
from hermes.storage.base import StorageBackend
from hermes.storage.errors import (
    DatasetAlreadyExistsError,
    DatasetNotFoundError,
    StorageCorruptionError,
    StorageReadError,
    StorageWriteError,
)
from hermes.storage.metadata import StorageInfo, StoredDatasetMetadata

_DATA_FILE = "data.parquet"
_DATA_FILES = ("data.parquet", "data.ipc")
_METADATA_FILE = "metadata.json"
_SAFE_NAME = re.compile(r"^[A-Za-z0-9._-]+$")


def _data_file_for(format: str) -> str:
    if format == "parquet":
        return "data.parquet"
    if format == "ipc":
        return "data.ipc"
    raise StorageWriteError(f"unsupported storage format {format!r}; expected 'parquet' or 'ipc'")


def _assert_safe_name(name: str) -> str:

    if not isinstance(name, str) or not name or not _SAFE_NAME.fullmatch(name) or name in {".", ".."}:
        raise StorageError(f"unsafe dataset name {name!r}")
    return name


def _now() -> datetime:
    return datetime.now(tz=UTC)


def _write_data(data: object, target: Path, format: str) -> None:
    if format == "ipc":
        if isinstance(data, pl.DataFrame):
            data.write_ipc(target)
        elif isinstance(data, pl.LazyFrame):
            data.sink_ipc(target)
        elif pa is not None and isinstance(data, pa.Table):
            pq.write_table(data, target, format="ipc")
        else:
            raise StorageWriteError(f"cannot persist data of type {type(data).__name__}; expected Polars/Arrow")
        return
    if isinstance(data, pl.DataFrame):
        data.write_parquet(target)
    elif isinstance(data, pl.LazyFrame):
        data.sink_parquet(target)
    elif pa is not None and isinstance(data, pa.Table):
        pq.write_table(data, target)
    else:
        raise StorageWriteError(f"cannot persist data of type {type(data).__name__}; expected Polars/Arrow")


def _read_data(path: Path, format: str) -> pl.DataFrame:
    read = pl.read_parquet if format == "parquet" else pl.read_ipc
    try:
        return read(path)
    except Exception as exc:
        raise StorageReadError(f"failed to read {format} file {path}: {exc}") from exc


def _stats_from_file(path: Path, format: str) -> tuple[int, int, list[dict[str, str]]]:
    scan = pl.scan_parquet(path) if format == "parquet" else pl.scan_ipc(path)
    schema = scan.collect_schema()
    rows = int(scan.select(pl.len()).collect().item())
    return rows, len(schema), [{"name": col, "dtype": str(dtype)} for col, dtype in schema.items()]


def _atomic_write(target: Path, writer) -> None:
    tmp = target.with_name(f".{target.stem}.{uuid.uuid4().hex}.tmp")
    try:
        writer(tmp)
        os.replace(tmp, target)
    finally:
        tmp.unlink(missing_ok=True)


def _dump(obj: Any) -> str:
    return json.dumps(asdict(obj), indent=2, default=str)


def _convert(tp: Any, value: Any) -> Any:
    if value is None:
        return None
    if tp is datetime and isinstance(value, str):
        return datetime.fromisoformat(value)
    if is_dataclass(tp) and isinstance(value, dict):
        return _revive(tp, value)  # type: ignore[arg-type]
    origin = get_origin(tp)
    if origin is Union or origin is UnionType:
        for arg in get_args(tp):
            if arg is not type(None):
                return _convert(arg, value)
        return value
    if origin is list:
        (arg,) = get_args(tp) or (Any,)
        return [_convert(arg, item) for item in value] if isinstance(value, list) else value
    if origin is tuple:
        args = get_args(tp)
        if isinstance(value, list) and len(args) == 2:
            return tuple(_convert(args[0], item) for item in value)
        return value
    if origin is dict:
        _, vt = get_args(tp) or (Any, Any)
        return {k: _convert(vt, item) for k, item in value.items()} if isinstance(value, dict) else value
    return value


def _revive(cls: Any, raw: Any) -> Any:
    if not isinstance(raw, dict) or not is_dataclass(cls):
        return raw
    hints = get_type_hints(cls)
    known = {f.name for f in fields(cls)}
    kwargs = {k: _convert(hints[k], v) for k, v in raw.items() if k in known and k in hints}
    return cast(type[Any], cls)(**kwargs)


class FilesystemStorage(StorageBackend):
    def __init__(self, root: str | Path | None = None) -> None:
        root = root if root is not None else get_config().storage_root
        self.root = Path(root).expanduser().resolve()

    @property
    def _datasets_dir(self) -> Path:
        return self.root / "datasets"

    def _path_for(self, name: str) -> Path:
        return self._datasets_dir / _assert_safe_name(name)

    def _find_data_path(self, name: str) -> Path | None:
        target_dir = self._path_for(name)
        for candidate in _DATA_FILES:
            if (target_dir / candidate).is_file():
                return target_dir / candidate
        return None

    def _metadata_path(self, name: str) -> Path:
        return self._path_for(name) / _METADATA_FILE

    def save(
        self,
        dataset: Dataset,
        name: str | None = None,
        overwrite: bool = False,
        format: str = "parquet",
    ) -> StorageInfo:
        data_file = _data_file_for(format)
        target_name = _assert_safe_name(dataset.name if name is None else name)
        if dataset.data is None:
            raise StorageWriteError(f"Dataset {target_name!r} has no in-memory data; load it first (dataset.load())")

        target_dir = self._path_for(target_name)
        data_path = target_dir / data_file
        metadata_path = target_dir / _METADATA_FILE

        created = _now()
        existed = self.exists(target_name)
        if existed and not overwrite:
            raise DatasetAlreadyExistsError(f"Dataset {target_name!r} already exists; use overwrite=True to replace it")
        if existed:
            created = self._load_metadata(target_name).created

        created_dir = not target_dir.exists()
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            _atomic_write(data_path, lambda tmp: _write_data(dataset.data, tmp, format))
            rows, columns, column_schema = _stats_from_file(data_path, format)
            stored = self._build_metadata(dataset, target_name, rows, columns, column_schema, created, format, data_file)
            _atomic_write(
                metadata_path,
                lambda tmp: tmp.write_text(_dump(stored), encoding="utf-8"),
            )
        except StorageError:
            if created_dir:
                shutil.rmtree(target_dir, ignore_errors=True)
            raise
        except Exception as exc:
            if created_dir:
                shutil.rmtree(target_dir, ignore_errors=True)
            raise StorageWriteError(f"failed to save dataset {target_name!r}: {exc}") from exc

        return self._info_from(stored, data_path)

    def _build_metadata(
        self,
        dataset: Dataset,
        name: str,
        rows: int,
        columns: int,
        column_schema: list[dict[str, str]],
        created: datetime,
        format: str = "parquet",
        data_file: str = "data.parquet",
    ) -> StoredDatasetMetadata:
        source = dataset.provenance.source or dataset.metadata.source
        return StoredDatasetMetadata(
            name=name,
            dataset_id=str(dataset.id) if dataset.id else None,
            version=dataset.version,
            schema_ref=dataset.schema_ref,
            format=format,
            data_file=data_file,
            source=source,
            row_count=rows,
            column_count=columns,
            column_schema=column_schema,
            created=created,
            modified=_now(),
            dataset_metadata=dataset.metadata,
            provenance=dataset.provenance,
            lineage=dataset.lineage,
            data_version=dataset.data_version,
        )

    def load(self, name: str) -> Dataset:
        data_path = self._find_data_path(name)
        metadata_path = self._metadata_path(name)
        if data_path is None or not metadata_path.is_file():
            self._raise_not_found_or_corrupt(name, data_path, metadata_path)

        stored = self._load_metadata(name)
        fmt = stored.format if stored.format in ("parquet", "ipc") else "parquet"
        data_path = data_path or self._path_for(name) / _data_file_for(fmt)
        data = _read_data(data_path, fmt)
        self._check_integrity(name, stored, data)
        return self._to_dataset(stored, data, data_path)

    def _check_integrity(self, name: str, stored: StoredDatasetMetadata, data: pl.DataFrame) -> None:
        if stored.row_count is None or stored.column_schema is None:
            return
        if data.height != stored.row_count or data.width != stored.column_count:
            raise StorageCorruptionError(
                f"dataset {name!r} shape mismatch: stored {stored.row_count}x{stored.column_count}, got {data.height}x{data.width}"
            )
        stored_columns = [entry["name"] for entry in stored.column_schema if "name" in entry]
        if stored_columns and data.columns != stored_columns:
            raise StorageCorruptionError(
                f"dataset {name!r} column mismatch: stored {stored_columns}, got {data.columns}"
            )

    def _raise_not_found_or_corrupt(self, name: str, data_path: Path | None, metadata_path: Path) -> None:
        target_dir = self._path_for(name)
        data_ok = data_path is not None
        if target_dir.is_dir() and (data_ok or metadata_path.is_file()):
            raise StorageCorruptionError(
                f"dataset {name!r} is incomplete (missing {'data' if not data_ok else 'metadata'})"
            )
        raise DatasetNotFoundError(f"Dataset {name!r} not found in storage")

    def _load_metadata(self, name: str) -> StoredDatasetMetadata:
        path = self._metadata_path(name)
        try:
            return _revive(StoredDatasetMetadata, json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError, TypeError) as exc:
            raise StorageCorruptionError(f"metadata for dataset {name!r} is corrupt") from exc

    def _to_dataset(self, stored: StoredDatasetMetadata, data: pl.DataFrame, data_path: Path) -> Dataset:
        return Dataset(
            id=uuid.UUID(stored.dataset_id) if stored.dataset_id else uuid.uuid4(),
            name=stored.name,
            version=stored.version or "0.0.1",
            schema_ref=stored.schema_ref,
            data_ref=str(data_path),
            data=data,
            metadata=stored.dataset_metadata or MetaData(),
            provenance=stored.provenance or Provenance(),
            lineage=stored.lineage or Lineage(),
            data_version=stored.data_version,
        )

    def exists(self, name: str) -> bool:
        target_dir = self._path_for(name)
        return target_dir.is_dir() and self._find_data_path(name) is not None and (target_dir / _METADATA_FILE).is_file()

    def delete(self, name: str) -> None:
        if not self.exists(name):
            raise DatasetNotFoundError(f"Dataset {name!r} not found in storage")
        shutil.rmtree(self._path_for(name))

    def list(self) -> list[str]:
        datasets_dir = self._datasets_dir
        if not datasets_dir.is_dir():
            return []
        names = []
        for entry in datasets_dir.iterdir():
            if entry.is_dir() and self._find_data_path(entry.name) is not None and (entry / _METADATA_FILE).is_file():
                names.append(entry.name)
        return sorted(names)

    def info(self, name: str) -> StorageInfo:
        if not self.exists(name):
            raise DatasetNotFoundError(f"Dataset {name!r} not found in storage")
        stored = self._load_metadata(name)
        fmt = stored.format if stored.format in ("parquet", "ipc") else "parquet"
        return self._info_from(stored, self._find_data_path(name) or self._path_for(name) / _data_file_for(fmt))

    def _info_from(self, stored: StoredDatasetMetadata, data_path: Path) -> StorageInfo:
        size = data_path.stat().st_size if data_path.is_file() else 0
        return StorageInfo(
            dataset=stored.name,
            format=stored.format,
            path=str(data_path),
            size=size,
            rows=stored.row_count,
            columns=stored.column_count,
            created=stored.created,
            modified=stored.modified,
            column_schema=stored.column_schema,
            version=stored.version,
            source=stored.source,
        )


__all__ = ["FilesystemStorage"]
