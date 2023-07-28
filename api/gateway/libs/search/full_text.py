import requests
import dependencies
from .base import BaseSearch


class FullTextSearch(BaseSearch):
    def __init__(self, index=None):
        """
         Initialize search object.
        """
        super().__init__(dependencies.SEARCH_URL, dependencies.SEARCH_TOKEN, "search")

    # def _index_check(self):
    #     resp = requests.head(self.url)
    #     return resp.status_code

    # def _create_index(self):
    #     if self._index_check() == 400:
    #         print('creating index', self.url)
    #         self.put()
    #         return True # this automatically creates the index
    #     return True
