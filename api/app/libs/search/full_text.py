import requests
import dependencies
from .base import BaseSearch


class FullTextSearch(BaseSearch):
    def __init__(self, index=None):
        """
        Initialize search object.
        """
        super().__init__(dependencies.SEARCH_URL, dependencies.SEARCH_TOKEN, "search")
