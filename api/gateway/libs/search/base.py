from typing import Optional
import requests

Response =  requests.models.Response

class BaseSearch:

    def __init__(self, url: str, token:Optional[str]=None, search_type:Optional[str]="search"):
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

    def get(self, params: dict) -> Response:
        """
         Get data from external search endpoint. This is a wrapper around requests. get that handles status codes that aren't 200
         
         @param params - Parameters to be passed to the request
         
         @return JSON response or error message if something went wrong
        """
        resp = requests.get(self.url, params=params, headers=self.headers)
        # Returns a JSON string with the response.
        if resp.status_code != 200: return {"detail": f"{self.search_type} query failed.", "status_code": resp.status_code}
        data = resp.json()
        return data

    def post(self, data: dict) -> Response:
        """
        Post data to external search endpoint. This is a wrapper around requests. post that handles errors and returns a dict with status code and error message
        
        @param data - dict to be sent as POST body
        
        @return dict with response from API or error message if status
        """
        resp = requests.post(self.url, data=data, headers=self.headers)
        # Returns a JSON string with the response.
        if resp.status_code >= 400: return {"detail": f"{self.search_type} query failed.", "status_code": resp.status_code}
        data = resp.json()
        return data
