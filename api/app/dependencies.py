import os

GEOCODING_URL = os.environ.get("GEOCODE_URL", "http://localhost:9000")
GEOCODING_TOKEN = os.environ.get("GEOCODING_TOKEN", None)

FASTAPI_SECRET_KEY = os.environ.get("FASTAPI_SECRET_KEY", "this1saveryS3creTKey000111")

SEARCH_URL = os.environ.get("SEARCH_URL", "http://localhost:8999")
SEARCH_TOKEN = os.environ.get("SEARCH_TOKEN", None)
REDIS_URL = os.environ.get("REDIS_URL", "http://localhost:5380")

POSTGRES_USER = os.environ.get("POSTGRES_USER", "therapease_user_dev")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSSWORD", "therapease_devpass")
POSTGRES_DB = os.environ.get("POSETGRES_DB", "therapease_db_dev")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
