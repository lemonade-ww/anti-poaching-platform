from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import scoped_session

from api.config import get_connection_string

# SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False))


def bind_session(session: scoped_session) -> Engine:
    """Initialize the engine and configure the SessionLocal factory

    Args:
        is_test (bool, optional): Whether to use the test configuration or not. Defaults to False.
    """
    conn = get_connection_string()
    engine = create_engine(url=conn)
    session.configure(bind=engine)
    return engine
