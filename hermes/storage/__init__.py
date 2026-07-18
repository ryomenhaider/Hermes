from __future__ import annotations

from pathlib import Path
from typing import Any

from hermes.database._sync import SyncDatabase
from hermes.storage._cache import RawCache
from hermes.storage._feature_store import FeatureStore
from hermes.storage._lineage import LineageGraph
from hermes.storage._metadata import MetadataRegistry


class StorageLayer:
    def __init__(self, db: SyncDatabase | None = None, cache_dir: str | Path | None = None):
        self._db = db
        self._cache = RawCache(cache_dir=cache_dir)
        self._features: FeatureStore | None = None
        self._metadata: MetadataRegistry | None = None
        self._lineage: LineageGraph | None = None

        if db is not None:
            self._features = FeatureStore(db)
            self._metadata = MetadataRegistry(db)
            self._lineage = LineageGraph(db)

    @property
    def cache(self) -> RawCache:
        return self._cache

    @property
    def features(self) -> FeatureStore:
        if self._features is None:
            raise RuntimeError("StorageLayer not connected to a database. Call .connect(db_url)")
        return self._features

    @property
    def metadata(self) -> MetadataRegistry:
        if self._metadata is None:
            raise RuntimeError("StorageLayer not connected to a database. Call .connect(db_url)")
        return self._metadata

    @property
    def lineage(self) -> LineageGraph:
        if self._lineage is None:
            raise RuntimeError("StorageLayer not connected to a database. Call .connect(db_url)")
        return self._lineage

    def connect(self, db_url: str, migrations_dir: str = "./migrations", **kwargs: Any) -> None:
        self._db = SyncDatabase(db_url, migrations_dir=migrations_dir, **kwargs)
        self._features = FeatureStore(self._db)
        self._metadata = MetadataRegistry(self._db)
        self._lineage = LineageGraph(self._db)


__all__ = [
    "FeatureStore",
    "LineageGraph",
    "MetadataRegistry",
    "RawCache",
    "StorageLayer",
]
