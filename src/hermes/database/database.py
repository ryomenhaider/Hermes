from __future__ import annotations

import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from hermes.config import DB_URL

logger = logging.getLogger(__name__)

DATABASE_URL = DB_URL or "sqlite+pysqlite:///./hermes.db"

class Base(DeclarativeBase):
    pass

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
)


def get_db() -> Session:
    return SessionLocal()


def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    import hermes.models.fred_model  

    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized using %s", DATABASE_URL)
