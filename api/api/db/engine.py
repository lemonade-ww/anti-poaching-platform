from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

from api.config import get_connection_string
from api.db.session import SessionLocal


def init_engine() -> Engine:
    conn = get_connection_string()
    engine = create_engine(url=conn)
    SessionLocal.configure(bind=engine, autocommit=False, autoflush=False)
    return engine
