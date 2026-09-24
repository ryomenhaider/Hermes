import hashlib
import io
import sqlite3
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import polars as pl
import pyarrow as pa

from hermes.core.errors import HermesError
from hermes.core.lineage import Lineage, LineageStep
from hermes.core.metadata import InspectReport, MetaData
from hermes.core.provenance import Provenance
from hermes.core.versioning import DataVersion


def frame_checksum(data: object) -> str:
    # ponytail: lazy frames are hashed by query plan, not content — hashing 33GB
    # of rows on every record() would defeat lazy loading. Swap to a streaming
    # content hash if version integrity requires it.
    if isinstance(data, pl.LazyFrame):
        return hashlib.sha256(data.explain().encode()).hexdigest()
    if isinstance(data, pl.DataFrame):
        buf = io.BytesIO()
        data.write_ipc(buf)
        return hashlib.sha256(buf.getvalue()).hexdigest()
    return hashlib.sha256(repr(data).encode()).hexdigest()


@dataclass
class Dataset:
    """Dataset is the central object; `.data` holds the payload and all
    container access (items, iteration, length, truthiness, attributes) is
    delegated to it so wrapped data stays usable as-is."""
    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    version: str = "0.0.1"

    data_ref: str | Path | None = None
    schema_ref: str | None = None
    data: Any = None

    metadata: MetaData = field(default_factory=MetaData)
    provenance: Provenance = field(default_factory=Provenance)
    lineage: Lineage = field(default_factory=Lineage)

    data_version: DataVersion | None = None

    def provenance_info(self) -> Provenance:
        if self.provenance is None:
            raise ValueError("No provenance Is stored")
        return self.provenance

    def lineage_info(self) -> Lineage:
        if self.lineage is None:
            raise ValueError("No lineage is stored")
        return self.lineage

    def schema_info(self) -> str | None:
        if self.schema_ref is None:
            raise ValueError("No Schema is stored")
        return self.schema_ref

    def metadata_info(self) -> MetaData:
        if self.metadata is None:
            raise ValueError("No MetaData Available")
        return self.metadata

    def record(
        self,
        operation: str,
        input_ref: str | None = None,
        params: dict | None = None,
        *,
        version: bool = True,
    ) -> "Dataset":
        self.lineage.add_step(
            LineageStep(
                operation=operation,
                input_ref=input_ref,
                output_ref=self.name,
                params=dict(params or {}),
            )
        )
        if version:
            self._bump_version()
        return self

    def _bump_version(self) -> None:
        if self.data is None:
            return
        prev = self.data_version
        frame = self.data if isinstance(self.data, pl.DataFrame) else None
        schema_hash = None
        if frame is not None:
            schema_hash = hashlib.sha256(str(sorted((c, str(t)) for c, t in frame.schema.items())).encode()).hexdigest()
        self.data_version = DataVersion(
            content_hash=frame_checksum(self.data),
            schema_hash=schema_hash,
            parent_version=prev.content_hash if prev else None,
        )

    def __getattr__(self, name: str) -> object:
        data = self.__dict__.get("data")
        if data is None or name.startswith("__"):
            raise AttributeError(name)
        return getattr(data, name)

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __contains__(self, item) -> bool:
        return item in self.data

    def __bool__(self) -> bool:
        return bool(self.data)

    def inspect(self) -> InspectReport:
        if self.data is None:
            raise HermesError("Load the data first (call .load()).")

        from hermes.api.data import inspect as inspect_data

        report = inspect_data(self.data)
        report.dataset_id = str(self.id)
        report.name = self.name
        report.version = self.version
        report.schema_ref = self.schema_ref
        report.stored_metadata = self.metadata
        report.provenance = self.provenance
        report.lineage = self.lineage
        return report

    def profile(self) -> MetaData:
        if self.data is None:
            raise HermesError("Load The Data First")

        from hermes.api.data import profile

        _profile = profile(self.data)
        self.set_metadata(_profile)
        self.record("profile", version=False)
        return self.metadata

    def set_metadata(self, metadata: MetaData) -> None:
        self.metadata = metadata

    def save(self, path: str, format: str = "parquet") -> None:
        if self.data is None:
            raise HermesError("Load The Data First")

        from hermes.export.utils import export as export_data

        export_data(
            data=self.to_polars(),
            filetype=format,
            loc=path,
            name=self.name,
        )

    def export(self, format: str = "parquet") -> object:
        if self.data is None:
            raise HermesError("Load The Data First")

        if format == "polars":
            return self.to_polars()
        if format == "arrow":
            return self.to_arrow()
        if format == "pandas":
            return self.to_pandas()

        import io

        df = self.to_polars()
        buffer = io.BytesIO()
        if format == "csv":
            df.write_csv(buffer)
        elif format == "json":
            df.write_json(buffer)
        elif format == "parquet":
            df.write_parquet(buffer)
        else:
            raise ValueError(f"Unsupported export format: {format}")

        return buffer.getvalue()

    def to_lazy(self) -> pl.LazyFrame:
        from hermes.parsing.engine import ParserEngine

        if isinstance(self.data, pl.LazyFrame):
            return self.data
        if isinstance(self.data, pl.DataFrame):
            return self.data.lazy()
        if self.data_ref is not None:
            scan = ParserEngine().scan(self.data_ref)
            if scan is not None:
                return scan
        return pl.DataFrame(self.data).lazy()

    def to_polars(self) -> pl.DataFrame:
        data = self.data

        if isinstance(data, pl.DataFrame):
            return data

        if isinstance(data, pl.LazyFrame):
            return data.collect()

        if isinstance(data, pa.Table):
            return pl.from_arrow(data)  # type: ignore[return-value]

        if isinstance(data, (list, dict)):
            return pl.DataFrame(data)

        raise TypeError(f"Cannot convert {type(data).__name__} to Polars")

    def to_pandas(self) -> object:
        return self.to_polars().to_pandas()

    def to_arrow(self) -> pa.Table:
        data = self.data

        if isinstance(data, pl.LazyFrame):
            data = data.collect()

        if isinstance(data, pl.DataFrame):
            return data.to_arrow()

        if isinstance(data, pa.Table):
            return data

        raise TypeError(f"Cannot convert {type(data).__name__} to Arrow")

    def load(self):
        if self.data_ref is None:
            raise HermesError("Dataset has no data_ref; provide a data_ref or call hr.load(name)")

        ref = str(self.data_ref)

        if ref.startswith(("postgres://", "postgresql://")):
            raise NotImplementedError("PostgreSQL sources are not supported yet; use hr.fetch()")

        elif ref.startswith("sqlite://"):
            connection = sqlite3.connect(ref.removeprefix("sqlite:///"))
            try:
                tables = pl.read_database(
                    query="SELECT name FROM sqlite_master WHERE type='table';", connection=connection
                )
                tables = tables["name"].to_list()

                data = {}

                for table in tables:
                    data[table] = pl.read_database(query=f"SELECT * FROM {table}", connection=connection)  # noqa: S608  # nosec B608

                data = pl.DataFrame(data)
            finally:
                connection.close()

        elif ref.startswith(("http://", "https://")):
            raise NotImplementedError("HTTP sources are not supported yet; use hr.fetch()")

        else:
            from hermes.parsing.engine import ParserEngine

            engine = ParserEngine()
            data = engine.scan(ref)
            if data is None:
                data = engine.parse(ref)

        self.data = data
        self.record("load", input_ref=ref)
        return self.data
