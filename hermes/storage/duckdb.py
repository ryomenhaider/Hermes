from hermes.storage.base import StorageBackend


class DuckDBStorage(StorageBackend):
    def __init__(self, database_path: str = "~/.hermes/data/hermes.duckdb") -> None:
        self.database_path = database_path

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

    def query(self, sql: str) -> object:
        raise NotImplementedError()
