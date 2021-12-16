import json
import os

import requests


class Requester:
    """乐健 API 请求者。"""

    def __init__(self) -> None:
        self.__read_config()

    def __read_config(self) -> None:
        """读取 API 与 headers 配置文件。"""
        try:
            with open(
                file=os.path.join("config", "api.json"),
                mode="r",
                encoding="utf-8",
            ) as fr:
                self.api_dict: dict[str, dict] = json.load(fr)

            with open(
                file=os.path.join("config", "headers.json"),
                mode="r",
                encoding="utf-8",
            ) as fr:
                self.headers: dict = json.load(fr)

        except FileNotFoundError:
            raise FileNotFoundError("config not found")

    def request(self, api_name: str, data: str = "") -> dict:
        """向指定 API 发起请求。

        Args:
            api_name: 指定 API 的名称。
            data: 要 POST / PUT 的数据。如果不需要，则默认为 ""。

        Returns:
            响应中的 data 字段。
        """
        api = self.api_dict[api_name]

        method = api["method"]
        if method == "get":
            response = requests.get(url=api["url"], headers=self.headers)
        elif method == "post":
            response = requests.post(url=api["url"], headers=self.headers, data=data)
        elif method == "put":
            response = requests.put(url=api["url"], headers=self.headers, data=data)
        else:
            raise Exception("invalid request type")

        return Requester.__parse_response_to_data(response)

    def get_api_data(self, api_name: str) -> dict:
        """获取指定 API 的 POST 数据。

        Args:
            api_name: 指定的 API 名称。

        Returns:
            该 API 的 POST 数据。
        """
        return self.api_dict[api_name]["data"]

    def update_api_data(self, api_name: str, new_data: dict) -> dict:
        """更新指定 API 的 POST 数据。

        Args:
            api_name: 指定 API 的名称。
            new_data: 要新增的数据。

        Returns:
            更新后的 POST 数据。
        """
        api = self.api_dict[api_name]
        api["data"].update(new_data)
        return api["data"]

    @staticmethod
    def __parse_response_to_data(response: requests.Response) -> dict:
        """解析出响应的 data 字段。

        Args:
            response: 站点的响应。

        Returns:
            响应中的 data 字段。
        """
        response_json = response.json()
        if response.status_code != 200:
            raise Exception(response_json["message"])

        try:
            data = response_json["data"]
        except KeyError:
            raise Exception("response has no key named 'data'")

        return data


if __name__ == "__main__":
    requester = Requester()
    print(requester.get_api_data("login"))
    print(requester.update_api_data("login", {"userName": "18962388966"}))
