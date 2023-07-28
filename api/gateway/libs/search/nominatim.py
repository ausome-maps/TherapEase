import dependencies
from .base import BaseSearch


class NominatimSearch(BaseSearch):
    def __init__(self):
        """
         Initialize geocoding service.
        """
        super().__init__(dependencies.GEOCODING_URL, dependencies.GEOCODING_TOKEN, "geocode")
 