from __future__ import annotations

import builtins

from hermes.datasets.models import DatasetDescriptor
from hermes.datasets.registry import DatasetRegistry
from hermes.storage.filesystem import FilesystemStorage
from hermes.storage.metadata import StorageInfo


def _descriptor_from_info(info: StorageInfo) -> DatasetDescriptor:
    return DatasetDescriptor(
        id=info.dataset,
        name=info.dataset,
        description="",
        source=info.source or "",
        schema_name=None,
        coverage=None,
        frequency=None,
        version=info.version or "0.0.1",
        quality=None,
    )


class DatasetCatalog:
    """In-memory descriptor index of stored datasets, fed from the storage backend."""

    def __init__(self, storage: FilesystemStorage | None = None) -> None:
        self._storage = storage or FilesystemStorage()
        self._registry = DatasetRegistry()

    def load(self) -> "DatasetCatalog":
        for name in self._storage.list():
            info = self._storage.info(name)
            self._registry.register(_descriptor_from_info(info))
        return self

    def list(self) -> builtins.list[DatasetDescriptor]:
        return self._registry.list_dataset()

    def get(self, dataset_id: str) -> DatasetDescriptor | None:
        return self._registry.get(dataset_id)

    def search(self, query: str) -> builtins.list[DatasetDescriptor]:
        return self._registry.search(query)

    def register(self, dataset: DatasetDescriptor) -> None:
        self._registry.register(dataset)


__all__ = ["DatasetCatalog"]