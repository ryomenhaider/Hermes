from __future__ import annotations

import builtins

from hermes.datasets.models import DatasetDescriptor


class DatasetRegistry:
    def __init__(self) -> None:
        self._datasets: dict[str, DatasetDescriptor] = {}

    def register(self, dataset: DatasetDescriptor) -> None:
        raise NotImplementedError()

    def get(self, dataset_id: str) -> DatasetDescriptor | None:
        raise NotImplementedError()

    def list(self) -> builtins.list[DatasetDescriptor]:
        raise NotImplementedError()

    def search(self, query: str) -> builtins.list[DatasetDescriptor]:
        raise NotImplementedError()
