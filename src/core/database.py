from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.core.config import settings

# Primary — for writes
engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)

# Replica — for reads (fallback to primary if not set)
read_engine = create_engine(
    settings.database_replica_url or settings.database_url,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
ReadSessionLocal = sessionmaker(bind=read_engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """Write session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_read_db():
    """Read-only session (uses replica)."""
    db = ReadSessionLocal()
    try:
        yield db
    finally:
        db.close()