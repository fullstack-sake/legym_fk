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
        self.__parse_content()

    def __parse_to_json(self) -> None:
        """Parse response to JSON form."""
        try:
            self.__body: dict = self.__response.json()
        except json.JSONDecodeError:
            raise LegymException(f"无法序列化的响应：{self.__response.text}")

    def __validate_status(self) -> None:
        """Validate status code of response."""
        status = self.__response.status_code
        if status == 200:
            return

        self.persistence()
        raise LegymException(self.__body.get("message", f"网络异常，状态码：{status}"))

    def __parse_content(self) -> None:
        """Parse code, message, data of response."""
        del self.__response

        try:
            self.__code: str = self.__body["code"]
            self.__message: str = self.__body["message"]
            self.__data: dict = self.__body["data"]

        except KeyError:
            self.persistence()
            raise LegymException("网站响应格式超出预期")

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
            raise LegymException(f"{self.__name} API 响应中的 `data` 没有 `{key}` 字段")
