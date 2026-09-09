from pydantic import BaseModel, Field
import uuid

from hermes.core.lineage import Lineage
from hermes.core.provenance import Provenance
from hermes.core.metadata import MetaData
from hermes.core.versioning import DataVersion


class Dataset(BaseModel):

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    version: str = "0.0.1"

    data_ref: str 
    schema_ref: str | None = None
    
    metadata: MetaData = Field(default_factory=MetaData)
    provenance: Provenance = Field(default_factory=Provenance)
    lineage: Lineage = Field(default_factory=Lineage)

    data_version: DataVersion | None = None

    def provenance_info(self) -> Provenance:
        ...

    def lineage_info(self) -> Lineage:
        ...

    def schema_info(self) -> str | None:
        ...

    def metadata_info(self) -> MetaData:
        ...

    def inspect(self) -> dict:
        ...

    def profile(self) -> dict:
        ...

    def save(self, path: str, format: str = "parquet") -> None:
        ...

    def export(self, format: str) -> object:
        ...

    def to_pandas(self) -> object:
        ...

    def to_polars(self) -> object:
        ...

    def to_arrow(self) -> object:
        ...
