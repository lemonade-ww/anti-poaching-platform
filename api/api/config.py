from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    pg_password: str
    pg_user: str
    pg_host: str
    pg_dbname: str

    class Config:
        # Database credentials should be retrieved
        # from the secret files mounted by Docker
        # under /run/secrets/
        secrets_dir: str = "/run/secrets"


@lru_cache()
def get_settings():
    return Settings()


@lru_cache()
def get_connection_string():
    settings = get_settings()
    return f"postgresql://{settings.pg_user}:{settings.pg_password}@{settings.pg_host}/{settings.pg_dbname}"
