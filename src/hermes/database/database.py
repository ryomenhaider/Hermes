from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from hermes.config import DB_URL

class Base(DeclarativeBase):
    pass

engine = create_engine(
    DB_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    return SessionLocal()


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()