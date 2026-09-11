import sqlite3
import uuid
from pathlib import Path

import polars as pl
import pyarrow as pa
from pydantic import BaseModel, ConfigDict, Field

from hermes.api.data import profile
from hermes.core.errors import HermesError
from hermes.core.lineage import Lineage, LineageStep
from hermes.core.metadata import InspectReport, MetaData
from hermes.core.provenance import Provenance
from hermes.core.versioning import DataVersion


class Dataset(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    version: str = "0.0.1"

    data_ref: str | Path
    schema_ref: str | None = None
    data: pl.DataFrame | None = None

    metadata: MetaData = Field(default_factory=MetaData)
    provenance: Provenance = Field(default_factory=Provenance)
    lineage: Lineage = Field(default_factory=Lineage)

    data_version: DataVersion | None = None

    def provenance_info(self) -> Provenance:
        if self.provenance is None:
            raise ValueError('No provenance Is stored')
        return self.provenance

    def lineage_info(self) -> Lineage:
        if self.lineage is None:
            raise ValueError('No lineage is stored')
        return self.lineage

    def schema_info(self) -> str | None:
        if self.schema_ref is None:
            raise ValueError('No Schema is stored')
        return self.schema_ref

    def metadata_info(self) -> MetaData:
        if self.metadata is None:
            raise ValueError('No MetaData Available')
        return self.metadata

    def inspect(self) -> InspectReport:
        if self.data is None:
            raise HermesError("Load the data first (call .load()).")

        columns = [(col, str(self.data.schema[col])) for col in self.data.columns]

        return InspectReport(
            dataset_id=str(self.id),
            name=self.name,
            version=self.version,
            schema_ref=self.schema_ref,
            row_count=self.data.height,
            column_count=self.data.width,
            columns=columns,
            stored_metadata=self.metadata,
            provenance=self.provenance,
            lineage=self.lineage,
            sample=self.data.head(5).to_dicts(),
        )

    def profile(self) -> MetaData:
        if self.data is None:
            raise HermesError("Load The Data First")

        _profile = profile(self.data)
        self.set_metadata(_profile)
        self.lineage.add_step(
            LineageStep(operation="profile", output_ref=self.name)
        )
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

    def to_polars(self) -> pl.DataFrame:
        data = self.data

        if isinstance(data, pl.DataFrame):
            return data

        if isinstance(data, pl.LazyFrame):
            return data.collect()

        if isinstance(data, pa.Table):
            return pl.from_arrow(data)  # type: ignore[return-value]

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
            data = self.__load_file()

        self.data = data
        self.lineage.add_step(
            LineageStep(operation="load", input_ref=ref, output_ref=self.name)
        )
        return self.data

    def __load_file(self):
        _path = Path(self.data_ref)
        suffix = _path.suffix.lower()
        if suffix == ".csv":
            return pl.read_csv(_path)
        if suffix == ".json":
            return pl.read_json(_path)
        if suffix == ".parquet":
            return pl.read_parquet(_path)
        if suffix in [".jsonl", ".ndjson"]:
            return pl.read_ndjson(_path)
        raise HermesError(f"{suffix} is not supported by Hermes yet")
