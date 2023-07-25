import requests


class BaseSearch:
    def __init__(self, url, token=None):
        self.url = url
        self.headers = {"Content-type": "application/json"}
        if token is not None:
            self.headers["Authorization"] = f"Token {token}"

    def get(self, params):
        return requests.get(self.url, params=params, headers=self.headers)

    def post(self, data):
        return requests.post(self.url, data=data, headers=self.headers)
