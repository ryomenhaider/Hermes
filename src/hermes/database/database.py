from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any, Generator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import select

from hermes.config import DB_URL

logger = logging.getLogger(__name__)



if not DB_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured. Please set DATABASE_URL to a PostgreSQL URI."
    )

Base = declarative_base()


class DatabaseSession:
    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._engine = create_async_engine(
            DB_URL,
            future=True,
            pool_pre_ping=True,
        )
        self._session = None

    def _get_session(self) -> AsyncSession:
        if self._session is None:
            self._session = self._loop.run_until_complete(self._create_session())
        return self._session

    async def _create_session(self) -> AsyncSession:
        session_factory = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            future=True,
        )
        return session_factory()

    def add(self, obj: Any) -> None:
        self._get_session().add(obj)

    def add_all(self, objects: list[Any]) -> None:
        self._get_session().add_all(objects)

    def merge(self, obj: Any) -> Any:
        return self._get_session().merge(obj)

    def commit(self) -> None:
        self._loop.run_until_complete(self._get_session().commit())

    def rollback(self) -> None:
        self._loop.run_until_complete(self._get_session().rollback())

    def refresh(self, obj: Any) -> None:
        self._loop.run_until_complete(self._get_session().refresh(obj))

    def close(self) -> None:
        if self._session is not None:
            self._loop.run_until_complete(self._session.close())
        self._loop.run_until_complete(self._engine.dispose())
        self._loop.close()


def get_db() -> DatabaseSession:
    return DatabaseSession()


def get_db_session() -> Generator[DatabaseSession, None, None]:
    db = get_db()
    try:
        yield db
    finally:
        db.close()


async def query_one_async(model: type[Any], **filters: Any) -> Any | None:
    engine = create_async_engine(DB_URL, future=True, pool_pre_ping=True)
    session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        future=True,
    )
    async with session_factory() as session:
        result = await session.execute(select(model).filter_by(**filters))
        value = result.scalars().first()
    await engine.dispose()
    return value


async def query_all_async(model: type[Any]) -> list[Any]:
    engine = create_async_engine(DB_URL, future=True, pool_pre_ping=True)
    session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        future=True,
    )
    async with session_factory() as session:
        result = await session.execute(select(model))
        value = list(result.scalars().all())
    await engine.dispose()
    return value


async def add_and_commit_async(obj: Any) -> Any:
    engine = create_async_engine(DB_URL, future=True, pool_pre_ping=True)
    session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        future=True,
    )
    async with session_factory() as session:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
    await engine.dispose()
    return obj


def query_one(model: type[Any], **filters: Any) -> Any | None:
    return asyncio.run(query_one_async(model, **filters))


def query_all(model: type[Any]) -> list[Any]:
    return asyncio.run(query_all_async(model))


def add_and_commit(obj: Any) -> Any:
    return asyncio.run(add_and_commit_async(obj))


async def run_migrations_async() -> None:
    migrations_dir = Path(__file__).resolve().parent / "migrations"
    migration_files = sorted(migrations_dir.glob("*.sql"))

    if not migration_files:
        logger.info("No SQL migration files found.")
        return

    engine = create_async_engine(DB_URL, future=True, pool_pre_ping=True)
    try:
        async with engine.begin() as connection:
            for migration_path in migration_files:
                logger.info("Running migration %s", migration_path.name)
                sql = migration_path.read_text(encoding="utf-8")
                statements = [
                    statement.strip()
                    for statement in sql.split(";")
                    if statement.strip() and not statement.strip().startswith("--")
                ]
                for statement in statements:
                    await connection.execute(text(statement))
    finally:
        await engine.dispose()

    logger.info("All migrations completed.")


async def init_db_async() -> None:
    import hermes.models.fred_model  # noqa: F401

    engine = create_async_engine(DB_URL, future=True, pool_pre_ping=True)
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    finally:
        await engine.dispose()

    await run_migrations_async()
    logger.info("Database initialized using %s", DB_URL)


def init_db() -> None:
    asyncio.run(init_db_async())

