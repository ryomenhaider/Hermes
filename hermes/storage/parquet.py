from hermes.storage.base import StorageBackend


class ParquetStorage(StorageBackend):
    def __init__(self, base_path: str = "~/.hermes/data") -> None:
        self.base_path = base_path

    def save(self, dataset: object, path: str) -> None:
        raise NotImplementedError()

    def load(self, path: str) -> object:
        raise NotImplementedError()

    def delete(self, path: str) -> None:
        raise NotImplementedError()

    def exists(self, path: str) -> bool:
        raise NotImplementedError()

    def list(self, prefix: str = "") -> list[str]:
        raise NotImplementedError()
