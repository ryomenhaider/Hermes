import logging
import sqlite3
import uuid
from pathlib import Path

import polars as pl
import pyarrow as pa
from pydantic import BaseModel, ConfigDict, Field

from hermes.core.lineage import Lineage
from hermes.core.metadata import MetaData
from hermes.core.provenance import Provenance
from hermes.core.versioning import DataVersion
from hermes.core.errors import HermesError

from hermes.api.data import profile

logger = logging.getLogger(__name__)


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
        return self.provenance

    def lineage_info(self) -> Lineage:
        return self.lineage

    def schema_info(self) -> str | None:
        return self.schema_ref

    def metadata_info(self) -> MetaData:
        return self.metadata

    def inspect(self) -> dict:
        raise NotImplementedError()

    def profile(self) -> dict:
        if self.data == None:
            raise HermesError('Load The Data First')
        return profile(self.data)

    def save(self, path: str, format: str = "parquet") -> None:
        raise NotImplementedError()

    def export(self, format: str) -> object:
        raise NotImplementedError()

    def to_polars(self) -> pl.DataFrame:
        data = self.data

        if isinstance(data, pl.DataFrame):
            return data

        if isinstance(data, pl.LazyFrame):
            return data.collect()

        if isinstance(data, pa.Table):
            return pl.from_arrow(data)  # type: ignore[return-value]

        raise TypeError(f"Cannot convert {type(data).__name__} to Polars")

    def to_arrow(self) -> object:
        data = self.data

        if isinstance(data, pl.DataFrame):
            return pa.Table(data)
        if isinstance(data, pl.LazyFrame):
            return pa.Table(data)
        if isinstance(data, pa.Table):
            return data

        raise TypeError(f"Cannot Convert {type(data).__name__} to Arrow")

    def load(self):
        ref = self.data_ref

        if ref.startswith(("postgres://", "postgresql://")):
            ...

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
            ...
        else:
            data = self.__load_file()

        self.data = data
        return data

    def __load_file(self):
        _path = Path(self.data_ref)
        path = _path.suffix.lower()
        supported_formats = [".csv", ".json", ".parquet", ".jsonl", ".ndjson"]
        if path in supported_formats:
            if path == ".csv":
                return pl.read_csv(path)
            if path == ".json":
                return pl.read_json(path)
            if path == ".parquet":
                return pl.read_parquet(path)
            if path in [".jsonl", ".ndjson"]:
                return pl.read_ndjson(path)
        else:
            logger.error(f"{path} is not supported by Hermes yet...")
