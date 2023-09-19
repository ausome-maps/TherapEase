from typing import Optional
import requests

Response = requests.models.Response
SEARCH_DEFAULT = "search"


class BaseSearch:
    def __init__(
        self,
        url: str,
        token: Optional[str] = None,
        search_type: Optional[str] = SEARCH_DEFAULT,
    ):
        """Initialize BaseSearch Class.

        Args:
            url (str): The URL.
            token (Optional[str], optional): The token. Defaults to None.
            search_type (Optional[str], optional): The search type. Defaults to "search".
        """
        self.url = url
        self.headers = {"Content-type": "application/json"}
        self.search_type = search_type
        # Set the Authorization header to the token.
        if token is not None:
            self.headers["Authorization"] = f"Token {token}"

    def get(self, params: dict, url: Optional[str] = None) -> Response:
        """
        Sends a GET request to the specified URL with the given parameters.

        Parameters:
            params (dict): The parameters to be sent with the request.
            url (Optional[str]): The URL to send the request to. If not provided, the class URL will be used.

        Returns:
            Response: The response object containing the JSON string with the response.

        Raises:
            Exception: If the request fails and the status code is not 200.

        Example:
            >>> params = {"key": "value"}
            >>> url = "https://example.com"
            >>> response = get(params, url)
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
        return resp.json()

    def post(self, data: dict, url: Optional[str] = None) -> Response:
        """
        Sends a POST request to the specified URL with the given query parameters and returns the response.

        Args:
            data (dict): The query parameters to send in the request.
            url (Optional[str]): The URL to send the request to. If not specified, the default URL will be used.

        Returns:
            Response: The response from the API call, as a JSON string. If the request is unsuccessful, a dictionary with details of the failure will be returned.
        """
        url_post = self.url
        if url is not None:
            url_post = url
        resp = requests.post(url_post, json=data, headers=self.headers)
        # Returns a JSON string with the response.
        if resp.status_code != 200:
            return {
                "detail": f"{self.search_type} query failed. Due to {resp.json()['error']}",
                "status_code": resp.status_code,
            }
        return resp.json()

    def put(self, data: dict, url: Optional[str] = None) -> Response:
        """
        Sends a PUT request to the specified URL with the provided data.

        Args:
            data (dict): The data to be sent in the request body.
            url (Optional[str]): The URL to send the PUT request to. If not provided, the default URL will be used.

        Returns:
            Response: The response object containing the JSON data returned by the request.

        Raises:
            dict: A dictionary with details about the failed query if the response status code is >= 400.

        Example Usage:
            >>> data = {"key": "value"}
            >>> response = put(data, "https://example.com/api")
        """
        url_put = self.url
        if url is not None:
            url_put = url
        resp = requests.put(url_put, json=data, headers=self.headers)
        # Returns a JSON string with the response.
        if resp.status_code >= 400:
            return {
                "detail": f"{self.search_type} query failed. Error: {resp.json()}",
                "status_code": resp.status_code,
            }
        return resp.json()
