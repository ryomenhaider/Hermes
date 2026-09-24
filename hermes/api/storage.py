from hermes.core.dataset import Dataset
from hermes.core.result import Result
from hermes.storage.filesystem import FilesystemStorage
from hermes.storage.metadata import StorageInfo


def _backend() -> FilesystemStorage:
    return FilesystemStorage()


def _failure(exc: BaseException) -> Result:
    result = Result(status="failure")
    result.add_error(exc)
    return result


def save(dataset: Dataset, name: str | None = None, overwrite: bool = False, format: str = "parquet") -> Result:
    try:
        info = _backend().save(dataset, name=name, overwrite=overwrite, format=format)
        return Result(
            status="success",
            data=info,
            statistics={
                "name": info.dataset,
                "rows": info.rows,
                "columns": info.columns,
                "path": info.path,
            },
        )
    except Exception as exc:  # noqa: BLE001 - all storage failures return as Result
        return _failure(exc)


def load(name: str) -> Result:
    """Reconstruct the Dataset stored under *name*; data lives in ``result.data``."""
    try:
        dataset = _backend().load(name)
    except Exception as exc:  # noqa: BLE001
        return _failure(exc)
    return Result(status="success", data=dataset, statistics={"name": name})


def exists(name: str) -> Result:
    try:
        found = _backend().exists(name)
    except Exception as exc:  # noqa: BLE001
        return _failure(exc)
    return Result(status="success", data=found, statistics={"name": name, "exists": found})


def delete(name: str) -> Result:
    try:
        _backend().delete(name)
    except Exception as exc:  # noqa: BLE001
        return _failure(exc)
    return Result(status="success", statistics={"name": name, "deleted": True})


def list_datasets() -> Result:
    try:
        names = _backend().list()
    except Exception as exc:  # noqa: BLE001
        return _failure(exc)
    return Result(status="success", data=names, statistics={"count": len(names)})


def storage_info(name: str) -> Result:
    try:
        info = _backend().info(name)
    except Exception as exc:  # noqa: BLE001
        return _failure(exc)
    return Result(status="success", data=info, statistics={"name": info.dataset})


__all__ = ["save", "load", "exists", "delete", "list_datasets", "storage_info", "StorageInfo"]