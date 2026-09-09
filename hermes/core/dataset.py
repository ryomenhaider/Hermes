from pathlib import Path
import io
import aiohttp
import polars as pl
import pyarrow as pa
from pydantic import BaseModel, Field
import logging
import uuid
import sqlite3

from hermes.core.lineage import Lineage
from hermes.core.provenance import Provenance
from hermes.core.metadata import MetaData
from hermes.core.versioning import DataVersion

logger = logging.getLogger(__name__)

class Dataset(BaseModel):

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
        data = self.data
        

    def profile(self) -> dict:
        ...

    def save(self, path: str, format: str = "parquet") -> None:
        ...

    def export(self, format: str) -> object:
        ...

    def to_polars(self) -> pl.DataFrame:
        data = self.data

        if isinstance(data, pl.DataFrame):
            return data

        if isinstance(data, pl.LazyFrame):
            return data.collect()

        if isinstance(data, pa.Table):
            return pl.from_arrow(data)

        raise TypeError(
            f"Cannot convert {type(data).__name__} to Polars"
        )


    def to_arrow(self) -> object:
        data = self.data

        if isinstance(data, pl.DataFrame):
            return pa.Table(data)
        if isinstance(data, pl.LazyFrame):
            return pa.Table(data)
        if isinstance(data, pa.Table):
            return data
        
        raise TypeError(
            f'Cannot Convert {type(data).__name__} to Arrow'
        )

    def load(self):
        ref = self.data_ref

        if ref.startswith(("postgres://", "postgresql://")):
            ...

        elif ref.startswith("sqlite://"):

            connection = sqlite3.connect(ref.removeprefix("sqlite:///"))
            try:
                tables = pl.read_database(
                    query="SELECT name FROM sqlite_master WHERE type='table';",
                    connection=connection
                )
                tables = tables['name'].to_list()
                
                data = {}

                for table in tables:
                    data[table] = pl.read_database(
                        query=f'SELECT * FROM {table}',
                        connection=connection
                    )
                
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
        supported_formats = ['.csv', '.json', '.parquet', '.jsonl', '.ndjson']
        if path in supported_formats:
            
            if path == '.csv':
                return pl.read_csv(path)
            if path == '.json':
                return pl.read_json(path)
            if path == '.parquet':
                return pl.read_parquet(path)
            if path in ['.jsonl', '.ndjson']:
                return pl.read_ndjson(path)
        else:
            logger.error(f'{path} is not supported by Hermes yet...')