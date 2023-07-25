import os
import dependencies
from .base import BaseSearch


class FullTextSeaerch(BaseSearch):
    def __init__(self):
        super().__init__(dependencies.SEARCH_URL, dependencies.SEARCH_TOKEN)
        self.search_type = "full-text"
