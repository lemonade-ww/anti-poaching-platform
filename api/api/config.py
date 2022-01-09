from configparser import Error
from enum import Enum
from functools import lru_cache
from os import error

from pydantic import BaseSettings, env_settings


class Environment(str, Enum):
    Production = "production"
    Development = "development"
    Testing = "testing"


class Settings(BaseSettings):
    pg_password: str
    pg_user: str
    pg_host: str
    pg_dbname: str
    pg_testhost: str | None
    pg_testdbname: str | None
    is_testing: bool = False
    environment: Environment = Environment.Development

    class Config:
        # Database credentials should be retrieved
        # from the secret files mounted by Docker
        # under /run/secrets/
        secrets_dir: str = "/run/secrets"


@lru_cache()
def get_settings():
    return Settings()


def get_connection_string():
    settings = get_settings()
    if settings.environment is Environment.Testing:
        host = settings.pg_testhost
        dbname = settings.pg_testdbname
    else:
        host = settings.pg_host
        dbname = settings.pg_dbname

    if dbname is None or host is None:
        raise ValueError("Host or database name is not configured")

    return f"postgresql://{settings.pg_user}:{settings.pg_password}@{settings.pg_host}/{dbname}"
