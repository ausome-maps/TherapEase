import os

GEOCODING_URL = os.environ.get("GEOCODE_URL", "http://localhost:9000")
GEOCODING_TOKEN = os.environ.get("GEOCODING_TOKEN", None)

SEARCH_URL = os.environ.get("SEARCH_URL", "http://localhost:8999")
SEARCH_TOKEN = os.environ.get("SEARCH_TOKEN", None)
