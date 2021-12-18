import json
import os

import requests

from legym.exception import LegymException


class LegymResponse:
    """Response returned by Legym API."""

    def __init__(self, response: requests.Response, name: str) -> None:
        """Validate and parse raw response.

        Args:
            response: Raw response returned by Legym API.
            name: Name to mark this piece of response.
        """
        self.__response = response
        self.__name = name
        self.__parse_to_json()
        self.__ensure_status()
        self.__ensure_data()

    def __parse_to_json(self) -> None:
        """Parse response to JSON form."""
        try:
            self.__body: dict = self.__response.json()
        except json.JSONDecodeError:
            raise LegymException(f"响应 {self.__name} 无法序列化：{self.__response.text}")

    def __ensure_status(self) -> None:
        """Ensure response status code equals 200."""
        status = self.__response.status_code
        if status == 200:
            return

        self.persist()
        raise LegymException(self.__body.get("message", f"网络异常，状态码：{status}"))

    def __ensure_data(self) -> None:
        """Ensure response JSON has key `data`."""
        if "data" in self.__body.keys():
            return

        self.persist()
        raise LegymException(f"响应 {self.__name} 没有 `data` 字段")

    def __getitem__(self, key: str):
        # Search in outer response.
        if key in self.__body.keys():
            return self.__body[key]

        # Search key inside `data`.
        if key in self.__body["data"].keys():
            return self.__body["data"][key]

        raise LegymException(f"{self.__name} API 的响应没有 `{key}` 字段")

    def persist(self) -> None:
        """Persist response JSON under directory /responses.

        Note:
            Mostly for debug purpose.
        """
        dirpath = "responses"
        filepath = os.path.join(dirpath, f"{self.__name}.json")

        if not os.path.exists(dirpath):
            os.mkdir(dirpath)

        with open(filepath, "w", encoding="utf-8") as fw:
            json.dump(self.__body, fw, ensure_ascii=False)
