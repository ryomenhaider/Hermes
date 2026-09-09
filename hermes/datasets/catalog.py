from __future__ import annotations

import builtins

from hermes.datasets.models import DatasetDescriptor
from hermes.datasets.registry import DatasetRegistry


class DatasetCatalog:
    def __init__(self) -> None:
        self._registry = DatasetRegistry()

    def list(self) -> builtins.list[DatasetDescriptor]:
        raise NotImplementedError()

    def get(self, dataset_id: str) -> DatasetDescriptor | None:
        raise NotImplementedError()

    def search(self, query: str) -> builtins.list[DatasetDescriptor]:
        raise NotImplementedError()

    def register(self, dataset: DatasetDescriptor) -> None:
        raise NotImplementedError()
