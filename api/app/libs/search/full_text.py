import requests
import dependencies
from .base import BaseSearch


class FullTextSearch(BaseSearch):
    def __init__(self):
        """
        Initialize search service.
        """
        super().__init__(dependencies.SEARCH_URL, dependencies.SEARCH_TOKEN, "search")
