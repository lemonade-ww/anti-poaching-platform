from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    pg_password: str
    pg_user: str
    pg_host: str
    pg_dbname: str
    pg_testdbname: str | None

    class Config:
        # Database credentials should be retrieved
        # from the secret files mounted by Docker
        # under /run/secrets/
        secrets_dir: str = "/run/secrets"


@lru_cache()
def get_settings():
    return Settings()


@lru_cache()
def get_connection_string(is_test: bool = False):
    settings = get_settings()
    dbname = settings.pg_testdbname if is_test else settings.pg_dbname
    if dbname is None:
        raise ValueError("Database name is not configured")
    return f"postgresql://{settings.pg_user}:{settings.pg_password}@{settings.pg_host}/{dbname}"
