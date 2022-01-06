from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

from api.config import get_settings
from api.db.session import SessionLocal


def init_engine() -> Engine:
    settings = get_settings()
    conn = f"postgresql://{settings.pg_user}:{settings.pg_password}@{settings.pg_host}/{settings.pg_dbname}"
    engine = create_engine(url=conn)
    SessionLocal.configure(bind=engine, autocommit=False, autoflush=False)
    return engine
