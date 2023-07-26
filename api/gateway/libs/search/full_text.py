import os
import dependencies
from .base import BaseSearch


class FullTextSeaerch(BaseSearch):
    def __init__(self):
        """
         Initialize search object. This is called from __init__ () and should not be called directly by user
        """
        super().__init__(dependencies.SEARCH_URL, dependencies.SEARCH_TOKEN)
        self.search_type = "full-text"
