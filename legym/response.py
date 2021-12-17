import json
import os

import requests


class LegymResponse:
    """Response returned by Legym API."""

    def __init__(self, response: requests.Response, name: str) -> None:
        self.__validate_status(response)
        self.__body = response.json()
        self.__primary_parse()
        self.__name = name

    def __validate_status(self, response: requests.Response) -> None:
        """Validate the status code of response.

        Args:
            response: The response to validate.
        """
        if response.status_code == 200:
            return

        try:
            response_json: dict = json.loads(response.text.encode("utf-8"))
        except json.JSONDecodeError:
            raise Exception(response.text)
        else:
            raise Exception(response_json.get("message", "network trouble"))

    def __primary_parse(self) -> None:
        """Parse code, message, data of response."""
        try:
            self.__code: str = self.__body["code"]
            self.__message: str = self.__body["message"]
            self.__data: dict = self.__body["data"]
        except KeyError:
            raise KeyError("irregular response structure")

    @property
    def code(self):
        """Set code as read-only."""
        return self.__code

    @property
    def message(self):
        """Set message as read-only."""
        return self.__message

    @property
    def data(self):
        """Set data as read-only."""
        return self.__data

    def persistence(self) -> None:
        """Response persistence.

        Note:
            Mostly for debug purpose.
        """
        dirpath = "responses"
        filepath = os.path.join(dirpath, f"{self.__name}.json")

        if not os.path.exists(dirpath):
            os.mkdir(dirpath)

        with open(filepath, "w", encoding="utf-8") as fw:
            json.dump(self.__body, fw, ensure_ascii=False)

    def get(self, key: str):
        """Get item in response data.

        Args:
            key: Key of demanded value.

        Returns:
            Value of the item.
        """
        try:
            return self.__data[key]
        except KeyError:
            raise KeyError(f"response <{self.__name}> has no key named '{key}'")
