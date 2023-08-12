import os
from fastapi_jwt import JwtRefreshBearer, JwtAccessBearer


GEOCODING_URL = os.environ.get("GEOCODE_URL", "http://localhost:9000")
GEOCODING_TOKEN = os.environ.get("GEOCODING_TOKEN", None)

SEARCH_URL = os.environ.get("SEARCH_URL", "http://localhost:8999")
SEARCH_TOKEN = os.environ.get("SEARCH_TOKEN", None)
REDIS_URL = os.environ.get("REDIS_URL", "http://localhost:5380")

SECRET_KEY = os.environ.get("FAST_API_SECRET_KEY", "mysecretkey123011")

access_security = JwtAccessBearer(secret_key=SECRET_KEY, auto_error=True)
refresh_security = JwtRefreshBearer(secret_key=SECRET_KEY, auto_error=True)
