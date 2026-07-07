## Its Shit (AI generated)
## i will clean this up after testing things 

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import select

from src.hermes.config import SUPABASE_DB_URL

logger = logging.getLogger(__name__)

Base = declarative_base()


def get_database_url() -> str | None:
    url = SUPABASE_DB_URL or os.getenv("DATABASE_URL")
    if not url:
        return None
    if url.startswith(("http://", "https://")):
        logger.warning(
            "SUPABASE_DB_URL looks like a Supabase site URL, not a Postgres connection string. "
            "Set SUPABASE_DB_URL to something like: "
            "postgresql+asyncpg://postgres:password@db.project.supabase.co:5432/postgres?sslmode=require"
        )
        return None
    return url


def _get_engine(database_url: str | None = None):
    url = database_url or get_database_url()
    if not url:
        raise RuntimeError(
            "SUPABASE_DB_URL is not configured. Please set SUPABASE_DB_URL to your Supabase Postgres URI."
        )
    connect_args = {"statement_cache_size": 0}
    if "sslmode=" in url:
        from urllib.parse import urlencode, parse_qs, urlparse, urlunparse
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        sslmode = params.pop("sslmode", [None])[0]
        if sslmode:
            connect_args["ssl"] = sslmode
        url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            urlencode(params, doseq=True),
            parsed.fragment
        ))
    return create_async_engine(url, future=True, pool_pre_ping=True, connect_args=connect_args)


def _get_session_factory(database_url: str | None = None):
    engine = _get_engine(database_url)
    session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        future=True,
    )
    return session_factory, engine


async def init_db_async(database_url: str | None = None) -> bool:
    url = database_url or get_database_url()
    if not url:
        logger.warning("No database URL configured; skipping database initialization.")
        return False

    engine = _get_engine(url)
    try:
        async with engine.begin() as connection:
            await connection.execute(text("SELECT 1"))
            await connection.run_sync(Base.metadata.create_all)
    finally:
        await engine.dispose()

    await run_migrations_async(database_url=url)
    logger.info("Database initialized using %s", url)
    return True


def init_db(database_url: str | None = None) -> bool:
    return asyncio.run(init_db_async(database_url))


async def run_migrations_async(database_url: str | None = None) -> None:
    url = database_url or get_database_url()
    if not url:
        logger.warning("No database URL configured; skipping migrations.")
        return

    migrations_dir = Path(__file__).resolve().parent / "migrations"
    migration_files = sorted(migrations_dir.glob("*.sql"))

    if not migration_files:
        logger.info("No SQL migration files found.")
        return

    engine = _get_engine(url)
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


async def save_one_async(obj: Any, database_url: str | None = None) -> Any:
    url = database_url or get_database_url()
    if not url:
        logger.warning("Skipping save because no valid database URL is configured.")
        return obj

    session_factory, engine = _get_session_factory(url)
    try:
        async with session_factory() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
    finally:
        await engine.dispose()


async def save_many_async(objects: list[Any], database_url: str | None = None) -> list[Any]:
    url = database_url or get_database_url()
    if not url:
        logger.warning("Skipping bulk save because no valid database URL is configured.")
        return objects

    session_factory, engine = _get_session_factory(url)
    try:
        async with session_factory() as session:
            session.add_all(objects)
            await session.commit()
            return objects
    finally:
        await engine.dispose()


async def fetch_all_async(model: type[Any], limit: int | None = None, **filters: Any) -> list[Any]:
    url = get_database_url()
    if not url:
        logger.warning("Skipping fetch because no valid database URL is configured.")
        return []

    session_factory, engine = _get_session_factory(url)
    try:
        async with session_factory() as session:
            result = await session.execute(select(model).filter_by(**filters))
            rows = result.scalars().all()
            if limit is not None:
                rows = rows[:limit]
            return list(rows)
    finally:
        await engine.dispose()


async def query_one_async(model: type[Any], **filters: Any) -> Any | None:
    rows = await fetch_all_async(model, limit=1, **filters)
    return rows[0] if rows else None


async def query_all_async(model: type[Any], limit: int | None = None, **filters: Any) -> list[Any]:
    return await fetch_all_async(model, limit=limit, **filters)


async def delete_many_async(model: type[Any], **filters: Any) -> None:
    url = get_database_url()
    if not url:
        logger.warning("Skipping delete because no valid database URL is configured.")
        return

    session_factory, engine = _get_session_factory(url)
    try:
        async with session_factory() as session:
            result = await session.execute(select(model).filter_by(**filters))
            rows = result.scalars().all()
            for row in rows:
                await session.delete(row)
            await session.commit()
    finally:
        await engine.dispose()


async def check_db_health_async(database_url: str | None = None) -> dict[str, Any]:
    url = database_url or get_database_url()
    if not url:
        return {
            "status": "not_configured",
            "database_url": None,
            "connected": False,
            "error": "SUPABASE_DB_URL is not configured",
        }

    engine = _get_engine(url)
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
            return {
                "status": "ok",
                "database_url": url,
                "connected": True,
            }
    except Exception as exc:
        logger.error("Database health check failed: %s", exc)
        return {
            "status": "error",
            "database_url": url,
            "connected": False,
            "error": str(exc),
        }
    finally:
        await engine.dispose()


def check_db_health(database_url: str | None = None) -> dict[str, Any]:
    return asyncio.run(check_db_health_async(database_url))

