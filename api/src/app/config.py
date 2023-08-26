import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GEOCODING_URL: str = os.environ.get("GEOCODE_URL", "http://localhost:9000")
    GEOCODING_TOKEN: str = os.environ.get("GEOCODING_TOKEN", "")
    FASTAPI_SECRET_KEY: str = os.environ.get(
        "FASTAPI_SECRET_KEY", "this1saveryS3creTKey000111"
    )

    SEARCH_URL: str = os.environ.get("SEARCH_URL", "http://localhost:8999")
    SEARCH_TOKEN: str = os.environ.get("SEARCH_TOKEN", "")
    REDIS_URL: str = os.environ.get("REDIS_URL", "http://localhost:5380")

    POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "therapease_user_dev")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSSWORD", "therapease_devpass")
    POSTGRES_DB: str = os.environ.get("POSETGRES_DB", "therapease_db_dev")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = os.environ.get("POSTGRES_PORT", 5432)


@lru_cache()
def get_settings():
    return Settings()
