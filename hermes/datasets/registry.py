from __future__ import annotations

import builtins

from hermes.datasets.models import DatasetDescriptor


class DatasetRegistry:
    def __init__(self) -> None:
        self._datasets: dict[str, DatasetDescriptor] = {}

    def register(self, dataset: DatasetDescriptor) -> None:
        if dataset.id in self._datasets and self._datasets[dataset.id] != dataset:
            raise ValueError(f"Dataset {dataset.id!r} already registered with a different descriptor")
        self._datasets[dataset.id] = dataset

    def get(self, dataset_id: str) -> DatasetDescriptor | None:
        return self._datasets.get(dataset_id)

    def list_dataset(self) -> builtins.list[DatasetDescriptor]:
        return sorted(self._datasets.values(), key=lambda d: d.name)

    def search(self, query: str) -> builtins.list[DatasetDescriptor]:
        needle = query.casefold()
        return [
            d
            for d in self.list_dataset()
            if any(needle in (value or "").casefold() for value in (d.name, d.description, d.source, d.schema_name))
        ]


__all__ = ["DatasetRegistry"]