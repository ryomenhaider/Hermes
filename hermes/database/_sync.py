from __future__ import annotations

import csv
from io import StringIO
from typing import Any, Iterator

from sqlalchemy import MetaData, Table, create_engine, delete, insert, select, text, update
from sqlalchemy.engine import Engine

from hermes.database._filters import FilterBuilder
from hermes.database._migrate import MigrationRunner


class SyncDatabase:
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

        self._engine: Engine = create_engine(url, **engine_kwargs)
        self._metadata = MetaData()
        self._filters = FilterBuilder(strict=strict_filters)

        runner = MigrationRunner(migrations_dir)
        with self._engine.begin() as conn:
            runner.apply(conn)

    def _reflect(self, table_name: str) -> Table:
        return Table(table_name, self._metadata, autoload_with=self._engine)

    def register_operator(self, name: str, fn: Any) -> None:
        self._filters._operators[name] = fn

    def insert(
        self, table_name: str, records: list[dict[str, Any]], *, batch_size: int = 50_000
    ) -> int:
        if not records:
            return 0

        if len(records) >= self.bulk_copy_threshold:
            return self._copy_insert(table_name, records)

        table = self._reflect(table_name)
        total = 0
        with self._engine.begin() as conn:
            for i in range(0, len(records), batch_size):
                batch = records[i : i + batch_size]
                conn.execute(insert(table), batch)
                total += len(batch)
        return total

    def _copy_insert(self, table_name: str, records: list[dict[str, Any]]) -> int:
        if not records:
            return 0

        columns = list(records[0].keys())
        buf = StringIO()
        writer = csv.DictWriter(buf, fieldnames=columns, extrasaction="ignore")
        writer.writerows(records)
        buf.seek(0)

        with self._engine.raw_connection() as raw_conn:
            with raw_conn.cursor() as cur:
                cur.copy_expert(
                    f"COPY {table_name} ({','.join(columns)}) FROM STDIN WITH CSV",
                    buf,
                )
            raw_conn.commit()

        return len(records)

    def upsert(
        self,
        table_name: str,
        records: list[dict[str, Any]],
        conflict_columns: list[str],
        *,
        batch_size: int = 50_000,
    ) -> int:
        if not records:
            return 0

        if len(records) >= self.bulk_copy_threshold:
            return self._copy_upsert(table_name, records, conflict_columns)

        table = self._reflect(table_name)
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
        with self._engine.begin() as conn:
            for i in range(0, len(records), batch_size):
                batch = records[i : i + batch_size]
                for record in batch:
                    conn.execute(stmt, record)
                total += len(batch)
        return total

    def _copy_upsert(
        self,
        table_name: str,
        records: list[dict[str, Any]],
        conflict_columns: list[str],
    ) -> int:
        if not records:
            return 0

        columns = list(records[0].keys())
        conflict_str = ", ".join(conflict_columns)
        update_str = ", ".join(
            f"{c}=excluded.{c}" for c in columns if c not in conflict_columns
        )

        buf = StringIO()
        writer = csv.DictWriter(buf, fieldnames=columns, extrasaction="ignore")
        writer.writerows(records)
        buf.seek(0)

        with self._engine.raw_connection() as raw_conn:
            with raw_conn.cursor() as cur:
                cur.execute(f"CREATE TEMP TABLE _upsert_staging (LIKE {table_name}) ON COMMIT DROP")
                cur.copy_expert(
                    f"COPY _upsert_staging ({','.join(columns)}) FROM STDIN WITH CSV",
                    buf,
                )
                cur.execute(
                    f"INSERT INTO {table_name} "
                    f"SELECT * FROM _upsert_staging "
                    f"ON CONFLICT ({conflict_str}) DO UPDATE SET {update_str}"
                )
            raw_conn.commit()

        return len(records)

    def update(
        self,
        table_name: str,
        filters: dict[str, Any],
        values: dict[str, Any],
    ) -> int:
        table = self._reflect(table_name)
        where = self._filters.build(table, filters)

        stmt = update(table).values(**values)
        if where is not None:
            stmt = stmt.where(where)

        with self._engine.begin() as conn:
            result = conn.execute(stmt)
        return result.rowcount

    def delete(
        self,
        table_name: str,
        filters: dict[str, Any],
    ) -> int:
        table = self._reflect(table_name)
        where = self._filters.build(table, filters)

        stmt = delete(table)
        if where is not None:
            stmt = stmt.where(where)

        with self._engine.begin() as conn:
            result = conn.execute(stmt)
        return result.rowcount

    def read(
        self,
        table_name: str,
        filters: dict[str, Any] | None = None,
        *,
        columns: list[str] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        batch_size: int | None = None,
    ) -> Iterator[list[dict[str, Any]]]:
        table = self._reflect(table_name)
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

        with self._engine.connect() as conn:
            result = conn.execute(stmt)
            batch: list[dict[str, Any]] = []
            keys = list(result.keys())
            for row in result:
                batch.append(dict(zip(keys, row)))
                if batch_size and len(batch) >= batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch

    def execute(self, sql: str, params: dict[str, Any] | None = None) -> Any:
        with self._engine.begin() as conn:
            return conn.execute(text(sql), params or {})

    def raw_connection(self) -> Any:
        return self._engine.raw_connection()

    def close(self) -> None:
        self._engine.dispose()
