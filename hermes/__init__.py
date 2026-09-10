from hermes.api.acquire import fetch, ingest, read, sync
from hermes.api.data import (
    anomaly_count,
    date_ranges,
    get_freqs,
    inspect,
    normalize,
    parse,
    profile,
    transform,
    validate,
)
from hermes.api.datasets import get_dataset, list_datasets, search_datasets
from hermes.api.entities import resolve_company, resolve_country, resolve_entity
from hermes.api.schemas import compare_schema, get_schema, migrate, register_schema
from hermes.api.storage import load, materialize, query, save
from hermes.core.config import configure, get_config
from hermes.core.dataset import Dataset
from hermes.core.errors import (
    AcquisitionError,
    AuthenticationError,
    ConfigError,
    ConnectorNotFoundError,
    HermesError,
    NormalizationError,
    ParseError,
    QueryError,
    SchemaError,
    StorageError,
    ValidationError,
)
from hermes.core.result import Result

__all__ = [
    # Fetching
    "fetch",
    "ingest",
    "read",
    "sync",
    # Data operations
    "parse",
    "normalize",
    "validate",
    "transform",
    "profile",
    "inspect",
    "get_freqs",
    "date_ranges",
    "anomaly_count",
    # Datasets
    "Dataset",
    "list_datasets",
    "get_dataset",
    "search_datasets",
    # Entities
    "resolve_entity",
    "resolve_country",
    "resolve_company",
    # Schemas
    "get_schema",
    "register_schema",
    "compare_schema",
    "migrate",
    # Storage
    "save",
    "load",
    "query",
    "materialize",
    # Config
    "configure",
    "get_config",
    # Core
    "Result",
    "HermesError",
    "AcquisitionError",
    "ParseError",
    "SchemaError",
    "NormalizationError",
    "ValidationError",
    "StorageError",
    "QueryError",
    "ConfigError",
    "ConnectorNotFoundError",
    "AuthenticationError",
]
