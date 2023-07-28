import os
import dependencies
from .base import BaseSearch


class FullTextSearch(BaseSearch):
    def __init__(self):
        """
         Initialize search object.
        """
        super().__init__(dependencies.SEARCH_URL, dependencies.SEARCH_TOKEN, "search")
