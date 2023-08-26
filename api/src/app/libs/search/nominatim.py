from app.config import get_settings
from .base import BaseSearch


class NominatimSearch(BaseSearch):
    def __init__(self):
        """
        Initialize geocoding service.
        """
        settings = get_settings()
        super().__init__(settings.GEOCODING_URL, settings.GEOCODING_TOKEN, "geocode")
