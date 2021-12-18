import json
import os

import requests

from legym.exception import LegymException


class LegymResponse:
    """Response returned by Legym API."""

    def __init__(self, response: requests.Response, name: str) -> None:
        self.__response = response
        self.__name = name
        self.__parse_to_json()
        self.__validate_status()

    def __parse_to_json(self) -> None:
        """Parse response to JSON form."""
        try:
            self.__body: dict = self.__response.json()
        except json.JSONDecodeError:
            raise LegymException(f"{self.__name} API 的响应无法序列化：{self.__response.text}")

        try:
            assert "data" in self.__body.keys()
        except AssertionError:
            raise LegymException(f"{self.__name} API 的响应没有 `data` 字段")

    def __validate_status(self) -> None:
        """Validate status code of response."""
        status = self.__response.status_code
        if status == 200:
            return

        self.persistence()
        raise LegymException(self.__body.get("message", f"网络异常，状态码：{status}"))

    def __getitem__(self, key: str):
        """Get item in response.

        Args:
            key: Key of demanded value.

        Returns:
            Value of the item.
        """
        # Search key in response.
        if key in self.__body.keys():
            return self.__body[key]

        # Search key in `data`.
        if key in self.__body["data"].keys():
            return self.__body["data"][key]

        raise LegymException(f"{self.__name} API 的响应没有 `{key}` 字段")

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
