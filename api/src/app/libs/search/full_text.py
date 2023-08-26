from app.config import get_settings
from .base import BaseSearch

settings = get_settings()


class FullTextSearch(BaseSearch):
    def __init__(self):
        """
        Initialize search service.
        """
        super().__init__(settings.SEARCH_URL, settings.SEARCH_TOKEN, "search")
