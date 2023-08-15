import json
from typing import Optional
import requests

Response = requests.models.Response


class BaseSearch:
    def __init__(
        self,
        url: str,
        token: Optional[str] = None,
        search_type: Optional[str] = "search",
    ):
        """
        Initialize the object with the url and token. This is the constructor for the Request

        @param url - The url to request from
        @param token - The token to use for this request if it
        """
        self.url = url
        self.headers = {"Content-type": "application/json"}
        self.search_type = search_type
        # Set the Authorization header to the token.
        if token is not None:
            self.headers["Authorization"] = f"Token {token}"

    def get(self, params: dict, url: Optional[str] = None) -> Response:
        """
        Get data from external search endpoint. This is a wrapper around requests. get that handles status codes that aren't 200

        @param params - Parameters to be passed to the request

        @return JSON response or error message if something went wrong
        """
        url_get = self.url
        if url is not None:
            url_get = url
        resp = requests.get(url_get, params=params, headers=self.headers)
        # Returns a JSON string with the response.
        if resp.status_code != 200:
            return {
                "detail": f"{self.search_type} query failed. Due to {resp.json()['error']}",
                "status_code": resp.status_code,
            }
        data = resp.json()
        return data

    def post(self, query: dict, url: Optional[str] = None) -> Response:
        url_get = self.url
        if url is not None:
            url_get = url
        print(query)
        resp = requests.get(url_get, json=query, headers=self.headers)
        print("boom")
        # Returns a JSON string with the response.
        if resp.status_code != 200:
            return {
                "detail": f"{self.search_type} query failed. Due to {resp.json()['error']}",
                "status_code": resp.status_code,
            }
        data = resp.json()
        print(data)
        return data

    def put(self, data: dict, url: Optional[str] = None) -> Response:
        """
        Put data to external search endpoint. This is a wrapper around requests. post that handles errors and returns a dict with status code and error message

        @param data - dict to be sent as POST body

        @return dict with response from API or error message if status
        """

        url_put = self.url
        if url is not None:
            url_put = url
        data = json.loads(data)
        resp = requests.put(url_put, json=data, headers=self.headers)
        # Returns a JSON string with the response.
        if resp.status_code >= 400:
            return {
                "detail": f"{self.search_type} query failed. Error: {resp.json()}",
                "status_code": resp.status_code,
            }
        data = resp.json()
        return data
