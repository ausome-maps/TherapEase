import os


GEOCODING_URL = os.environ.get("GEOCODE_URL", "http://localhost:9000")
GEOCODING_TOKEN = os.environ.get("GEOCODING_TOKEN", None)

SEARCH_URL = os.environ.get("SEARCH_URL", "http://localhost:8999")
SEARCH_TOKEN = os.environ.get("SEARCH_TOKEN", None)
REDIS_URL = os.environ.get("REDIS_URL", "http://localhost:5380")

SECRET_KEY = os.environ.get("FAST_API_SECRET_KEY", "mysecretkey123011")

MONGO_INITDB_ROOT_USERNAME = os.environ.get(
    "MONGO_INITDB_ROOT_USERNAME", "therapease_mongo_user"
)
MONGO_INITDB_ROOT_PASSWORD = os.environ.get(
    "MONGO_INITDB_ROOT_PASSWORD", "therapease_mongo_password"
)
MONGO_INITDB_DATABASE = os.environ.get("MONGO_INITDB_DATABASE", "therapease_db")
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost:6000")

DATABASE_URL = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGO_HOST}:27017/{MONGO_INITDB_DATABASE}?authSource=admin"

ACCESS_TOKEN_EXPIRES_IN = 15
REFRESH_TOKEN_EXPIRES_IN = 60
JWT_ALGORITHM = "HS256"
