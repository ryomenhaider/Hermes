from __future__ import annotations

import asyncio
from typing import Any, Generic, TypeVar

from src.hermes.database.database import delete_many_async, fetch_all_async, save_many_async, save_one_async

ModelT = TypeVar("ModelT")


class AsyncRepository(Generic[ModelT]):
    """Small compatibility wrapper around the simple database helpers."""

    def __init__(self, model_cls: type[ModelT]) -> None:
        self.model_cls = model_cls

    def create_sync(self, obj: ModelT) -> ModelT:
        return asyncio.run(save_one_async(obj))

    def create_many_sync(self, objects: list[ModelT]) -> list[ModelT]:
        return asyncio.run(save_many_async(objects))

    def get_one_sync(self, **filters: Any) -> ModelT | None:
        rows = asyncio.run(fetch_all_async(self.model_cls, limit=1, **filters))
        return rows[0] if rows else None

    def get_all_sync(self, limit: int | None = None, **filters: Any) -> list[ModelT]:
        return asyncio.run(fetch_all_async(self.model_cls, limit=limit, **filters))

    def delete_sync(self, **filters: Any) -> None:
        asyncio.run(delete_many_async(self.model_cls, **filters))
