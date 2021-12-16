import json
import random
from datetime import datetime, timedelta
from math import dist
from os import altsep, popen

from requester import Requester


class LegymApp:
    """乐健破解程序。"""

    def __init__(self) -> None:
        self.requester = Requester()

    def get_user_id(self, username: str, password: str) -> str:
        """获取用户 ID。"""
        # 更新 POST 数据中的账号密码。
        post_data = self.requester.update_api_data(
            "login", {"userName": username, "password": password}
        )
        # 发起请求，并获得 token 和组织。
        login_data = self.requester.request("login", data=json.dumps(post_data))
        # 更新 headers 中的 token 和组织。
        self.requester.headers.update(
            {
                "authorization": f"Bearer {login_data['accessToken']}",
                "Organization": login_data["schoolId"],
            }
        )
        return login_data["id"]

    def get_semester(self) -> None:
        """获取学期。"""
        # 发起请求，并获得学期。
        return self.requester.request("semester")["id"]

    def get_limit(self) -> None:
        """获取跑步里程上限。"""
        # 发起请求，并获得里程上限。
        post_data = self.requester.get_api_data("limit")
        limit_data = self.requester.request("limit", data=json.dumps(post_data))
        return limit_data["limitationsGoalsSexInfoId"]

    def get_activities(self) -> list[dict]:
        """获取活动列表。

        Returns:
            活动列表。
        """
        post_data = self.requester.get_api_data("activities")
        activities_data = self.requester.request(
            "activities", data=json.dumps(post_data)
        )
        return activities_data["items"]

    def get_certain_activity_id(self, activity_name: str) -> str:
        """获取指定活动的 ID。

        Args:
            activity_name: 指定活动的名称。

        Returns:
            该活动的 ID。
        """
        # 从列表中筛选出目标活动。
        try:
            target: dict = list(
                filter(
                    lambda item: item["state"] == 4
                    and item["name"].find(activity_name) != -1,
                    self.get_activities(),
                )
            )[0]
        except IndexError:
            raise IndexError(f"activity '{activity_name}' not found")

        return target["id"]

    def get_all_activity_ids(self) -> list[str]:
        """获取所有活动的 ID。

        Returns:
            所有活动的 ID。
        """
        return [activity["id"] for activity in self.get_activities()]

    def sign_up(self, activity_id: str) -> bool:
        """报名指定活动。

        Args:
            activity_id: 指定活动的 ID。
        """
        self.requester.update_api_data("signUp", {"activityId": activity_id})
        post_data = self.requester.get_api_data("signUp")
        signup_data = self.requester.request("signUp", data=json.dumps(post_data))
        return signup_data["success"]

    def sign_in(self, activity_id: str) -> bool:
        """签到指定活动。

        Args:
            activity_id: 指定活动的 ID。
        """
        self.requester.update_api_data("signIn", {"activityId": activity_id})
        post_data = self.requester.get_api_data("signIn")
        signin_data = self.requester.request("signIn", data=json.dumps(post_data))
        return signin_data["message"] == "成功"

    def jogging(self, distance: float) -> bool:
        """跑步指定里程。

        Args:
            distance: 里程。
        """
        now = datetime.now()
        jogging_time = random.randint(20, 30)
        post_data = self.requester.update_api_data(
            "upload",
            {
                "startTime": (now - timedelta(minutes=jogging_time)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "totalMileage": distance,
                "avePace": jogging_time * 60 / distance * 1000
                + random.randint(0, 1) / 10,
                "calorie": int(distance * random.uniform(70.0, 75.0)),
                "effectiveMileage": distance,
                "endTime": now.strftime("%Y-%m-%d %H:%M:%S"),
                "gpsMileage": distance,
                "paceNumber": distance * (random.randint(50, 150)),
                "paceRange": random.randint(5, 10),
            },
        )
        upload_data = self.requester.request("upload", json.dumps(post_data))
        return upload_data

    def run(self) -> None:
        """运行程序。"""
        # 获取并更新用户 ID。
        user_id = self.get_user_id("18962388966", "siaoca708401")
        self.requester.update_api_data("signIn", {"userId": user_id})
        # 获取并更新当前学期。
        semester = app.get_semester()
        self.requester.update_api_data("limit", {"semesterId": semester})
        self.requester.update_api_data("upload", {"semesterId": semester})
        # 获取并更新里程上限。
        limit = self.get_limit()
        self.requester.update_api_data("upload", {"limitationsGoalsSexInfoId": limit})
        # 获取并更新指定活动 ID。
        # activity_id = self.get_certain_activity_id("第三空间清水河体育场")
        # print(self.sign_up(activity_id))
        # print(self.sign_in(activity_id))
        # 跑步。
        self.jogging(0.3)


if __name__ == "__main__":
    app = LegymApp()
    app.run()
