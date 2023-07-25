import os
import dependencies
from .base import BaseSearch


class NominatimSeaerch(BaseSearch):
    def __init__(self):
        super().__init__(dependencies.GEOCODING_URL, dependencies.GEOCODING_TOKEN)
        self.search_type = "geocoding"
