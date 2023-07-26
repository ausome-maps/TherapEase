import dependencies
from .base import BaseSearch


class NominatimSeaerch(BaseSearch):
    def __init__(self):
        """
         Initialize geocoding service. This is called by __init__ () and should not be called directly
        """
        super().__init__(dependencies.GEOCODING_URL, dependencies.GEOCODING_TOKEN)
        self.search_type = "geocoding"
