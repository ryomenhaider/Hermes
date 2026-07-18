from __future__ import annotations

from typing import Any, AsyncIterator

from sqlalchemy import MetaData, Table, delete, insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from hermes.database._filters import FilterBuilder
from hermes.database._migrate import MigrationRunner


class AsyncDatabase:
    def __init__(
        self,
        url: str,
        migrations_dir: str = "./migrations",
        bulk_copy_threshold: int = 500_000,
        strict_filters: bool = False,
        **engine_kwargs: Any,
    ):
        self.url = url
        self.migrations_dir = migrations_dir
        self.bulk_copy_threshold = bulk_copy_threshold
        self.strict_filters = strict_filters

        self._engine: AsyncEngine = create_async_engine(url, **engine_kwargs)
        self._metadata = MetaData()
        self._filters = FilterBuilder(strict=strict_filters)
        self._session_factory = async_sessionmaker(
            self._engine, expire_on_commit=False
        )
        self._reflect_cache: dict[str, Table] = {}

        self._initialized = False

    async def initialize(self) -> None:
        if self._initialized:
            return
        runner = MigrationRunner(self.migrations_dir)
        async with self._engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: runner.apply(sync_conn))
        self._initialized = True

    async def _reflect(self, table_name: str) -> Table:
        if table_name in self._reflect_cache:
            return self._reflect_cache[table_name]

        async with self._engine.begin() as conn:
            table = await conn.run_sync(
                lambda sync_conn: Table(
                    table_name, self._metadata, autoload_with=sync_conn
                )
            )
        self._reflect_cache[table_name] = table
        return table

    def register_operator(self, name: str, fn: Any) -> None:
        self._filters._operators[name] = fn

    async def insert(
        self, table_name: str, records: list[dict[str, Any]], *, batch_size: int = 50_000
    ) -> int:
        if not records:
            return 0

        table = await self._reflect(table_name)
        total = 0
        async with self._session_factory() as session:
            for i in range(0, len(records), batch_size):
                batch = records[i : i + batch_size]
                await session.execute(insert(table), batch)
                total += len(batch)
            await session.commit()
        return total

    async def upsert(
        self,
        table_name: str,
        records: list[dict[str, Any]],
        conflict_columns: list[str],
        *,
        batch_size: int = 50_000,
    ) -> int:
        if not records:
            return 0

        table = await self._reflect(table_name)
        columns = [c.name for c in table.columns]
        update_cols = [c for c in columns if c not in conflict_columns]
        conflict_str = ", ".join(conflict_columns)
        update_str = ", ".join(f"{c}=excluded.{c}" for c in update_cols)
        placeholders = ", ".join(f":{c}" for c in columns)
        col_names = ", ".join(columns)

        stmt = text(
            f"INSERT INTO {table_name} ({col_names}) "
            f"VALUES ({placeholders}) "
            f"ON CONFLICT ({conflict_str}) DO UPDATE SET {update_str}"
        )

        total = 0
        async with self._session_factory() as session:
            for i in range(0, len(records), batch_size):
                batch = records[i : i + batch_size]
                for record in batch:
                    await session.execute(stmt, record)
                total += len(batch)
            await session.commit()
        return total

    async def update(
        self,
        table_name: str,
        filters: dict[str, Any],
        values: dict[str, Any],
    ) -> int:
        table = await self._reflect(table_name)
        where = self._filters.build(table, filters)

        stmt = update(table).values(**values)
        if where is not None:
            stmt = stmt.where(where)

        async with self._session_factory() as session:
            result = await session.execute(stmt)
            await session.commit()
        return result.rowcount

    async def delete(
        self,
        table_name: str,
        filters: dict[str, Any],
    ) -> int:
        table = await self._reflect(table_name)
        where = self._filters.build(table, filters)

        stmt = delete(table)
        if where is not None:
            stmt = stmt.where(where)

        async with self._session_factory() as session:
            result = await session.execute(stmt)
            await session.commit()
        return result.rowcount

    async def read(
        self,
        table_name: str,
        filters: dict[str, Any] | None = None,
        *,
        columns: list[str] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        batch_size: int | None = None,
    ) -> AsyncIterator[list[dict[str, Any]]]:
        table = await self._reflect(table_name)
        col_objs = (
            [table.columns[c] for c in columns]
            if columns
            else list(table.columns)
        )
        stmt = select(*col_objs)
        where = self._filters.build(table, filters)
        if where is not None:
            stmt = stmt.where(where)
        if order_by is not None:
            stmt = stmt.order_by(text(order_by))
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)

        if batch_size:
            stmt = stmt.execution_options(yield_per=batch_size)

        async with self._session_factory() as session:
            result = await session.stream(stmt)
            batch: list[dict[str, Any]] = []
            keys = list(result.keys())
            async for row in result:
                batch.append(dict(zip(keys, row)))
                if batch_size and len(batch) >= batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch

    async def execute(self, sql: str, params: dict[str, Any] | None = None) -> Any:
        async with self._engine.begin() as conn:
            return await conn.execute(text(sql), params or {})

    async def close(self) -> None:
        await self._engine.dispose()
