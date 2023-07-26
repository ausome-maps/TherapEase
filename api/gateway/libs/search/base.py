from typing import Optional
import requests

Response =  requests.models.Response

class BaseSearch:

    def __init__(self, url: str, token:Optional[str]=None):
        """
         Initialize the object with the url and token. This is the constructor for the Request
         
         @param url - The url to request from
         @param token - The token to use for this request if it
        """
        self.url = url
        self.headers = {"Content-type": "application/json"}
        # Set the Authorization header to the token.
        if token is not None:
            self.headers["Authorization"] = f"Token {token}"

    def get(self, params: dict) -> Response:
        """
         Make a GET request to the API. This is a convenience method for requests.
         
         @param params - Parameters to be sent with the request. These will be encoded as query parameters in the request
         
         @return : class : ` Response `
        """
        return requests.get(self.url, params=params, headers=self.headers)

    def post(self, data: dict) -> Response:
        """
         Send a POST request to the API. This is a convenience method for making a POST request to the API and returning the response object
         
         @param data - The data to send in the request
         
         @return The response object from the API or None if something
        """
        return requests.post(self.url, data=data, headers=self.headers)
