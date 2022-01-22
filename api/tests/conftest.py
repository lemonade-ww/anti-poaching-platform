import os
from configparser import Error

import pytest
from fastapi.testclient import TestClient

from api.config import Environment, Settings, get_settings
from api.db.engine import bind_session
from api.db.models import Base
from api.db.session import SessionLocal
from api.dependencies import get_db
from api.main import app


@pytest.fixture(scope="session", autouse=True)
def settings():
    settings = get_settings()
    if settings.environment is not Environment.Development:
        raise Error(
            f"Testing environment is only available in {Environment.Development} environment"
        )
    os.environ["ENVIRONMENT"] = Environment.Testing
    get_settings.cache_clear()
    return get_settings()


@pytest.fixture(scope="session", autouse=True)
def engine(
    settings: Settings,
):  # Make sure that we update the environment to testing before setting up the engine
    assert settings.environment == Environment.Testing
    return bind_session(SessionLocal)


@pytest.fixture(scope="session", autouse=True)
def test_db(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function", autouse=True)
def client():
    session = SessionLocal()
    session.commit = session.flush

    def get_db_override():
        yield session

    app.dependency_overrides[get_db] = get_db_override

    yield TestClient(app)

    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
