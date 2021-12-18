import json
import os

import requests

from legym.response import LegymResponse


class LegymRequester:
    """Legym API requester."""

    def __init__(self) -> None:
        """Read configurations."""
        self.__read_api()
        self.__read_headers()

    def __read_api(self) -> None:
        """Read API configuration and store in a dictionary,
        which structured as:
        ```
        {
            "name": {
                "url": "https://example.com",
                "method": "get/post/put",
                "data": {},
                "description": "Description of this API"
            }
        }
        ```
        """
        api_path = os.path.join("config", "api.json")

        try:
            with open(api_path, "r", encoding="utf-8") as fr:
                self._api_dict: dict[str, dict] = json.load(fr)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"API config not found under path '{api_path}'"
            ) from None

    def __read_headers(self) -> None:
        """Read headers configuration."""
        headers_path = os.path.join("config", "headers.json")

        try:
            with open(headers_path, "r", encoding="utf-8") as fr:
                self._headers: dict = json.load(fr)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Headers config not found under path '{headers_path}'"
            ) from None

    def request(self, api_name: str) -> LegymResponse:
        """Issue a request.

        Args:
            api_name: Name of API, to which the request is issued.

        Returns:
            Processed response.
        """
        api = self._api_dict[api_name]
        url = api["url"]
        method = api["method"]
        data = json.dumps(api["data"])

        if method == "get":
            response = requests.get(url, headers=self._headers)
        elif method == "post":
            response = requests.post(url, data, headers=self._headers)
        elif method == "put":
            response = requests.put(url, data, headers=self._headers)
        else:
            raise Exception("invalid request type")

        return LegymResponse(response, name=api_name)

    def _update_api(self, api_name: str, new_data: dict) -> None:
        """Update data of API.

        Args:
            api_name: Name of API, of which the data will be updated.
            new_data: New data to add.
        """
        cur_data: dict = self._api_dict[api_name]["data"]
        cur_data.update(new_data)
