import random
from datetime import datetime, timedelta

from legym.activities import *
from legym.exception import LegymException
from legym.requester import LegymRequester


class LegymHacker(LegymRequester):
    """Legym hacker application."""

    def __init__(self) -> None:
        super().__init__()

    def __request_semester(self) -> None:
        """Get semester ID and update relevant API."""
        response = self.request("semester")
        semester_id: str = response["id"]
        self._update_api("limit", {"semesterId": semester_id})
        self._update_api("running", {"semesterId": semester_id})

    def __request_limit(self) -> None:
        """Get mileage limit and update relevant API."""
        response = self.request("limit")
        limit_id: str = response["limitationsGoalsSexInfoId"]
        self.__limit: float = response["effectiveMileageEnd"]
        self._update_api("running", {"limitationsGoalsSexInfoId": limit_id})

    def __get_first_available_activity(self) -> LegymActivity:
        """Get first available activity.

        Returns:
            Activity object.
        """
        available_activities = self._activities.search(state=ActivityState.available)

        if len(available_activities) == 0:
            raise LegymException("当前没有可报名的活动")
        else:
            return available_activities[0]

    def __get_specified_activity(self, activity_name: str) -> LegymActivity:
        """Get specified activity.

        Args:
            activity_name: Name of activity.

        Returns:
            Activity object.
        """
        specified_activities = self._activities.search(name=activity_name)

        if len(specified_activities) == 0:
            raise LegymException(f"找不到活动：{activity_name}")
        else:
            return specified_activities[0]

    def __register_with_id(self, activity_id: str) -> tuple[bool, str]:
        """Register activity with ID.

        Args:
            activity_id: Activity ID.

        Returns:
            - [0] `True` on success, or `False` on failure.
            - [1] Reason of success or failure.
        """
        self._update_api("register", {"activityId": activity_id})
        response = self.request("register")
        return response["success"], response["reason"]

    def __sign_with_id(self, activity_id: str) -> str:
        """Sign in activity with ID.

        Args:
            activity_id: Activity ID.

        Returns:
            Response message.
        """
        self._update_api("sign", {"activityId": activity_id})
        response = self.request("sign")
        return response["message"]

    def login(self, username: str, password: str) -> tuple[str, str]:
        """Log in Legym account.

        Args:
            username: Legym username.
            password: Legym password.

        Returns:
            - [0] User name.
            - [1] School name.
        """
        self._update_api("login", {"userName": username, "password": password})
        response = self.request("login")

        self._headers.update(
            {
                "authorization": f"Bearer {response['accessToken']}",
                "Organization": response["schoolId"],
            }
        )
        self._update_api("sign", {"userId": response["id"]})
        self.__request_semester()
        self.__request_limit()
        self._activities = self.get_activities()

        return response["realName"], response["schoolName"]

    def get_activities(self) -> LegymActivities:
        """Get activity list.

        Returns:
            Legym Activities object.
        """
        response = self.request("activities")
        return LegymActivities(response["items"])

    def register(self, activity_name: str = "") -> tuple[str, bool, str]:
        """Register activity.

        Args:
            activity_name: Name of activity to register,
            default to "", in which case the first available
            activity will be registered.

        Returns:
            - [0] Actual registered activity name.
            - [1] `True` on success, or `False` on failure.
            - [2] Reason of success or failure.
        """
        activity = (
            self.__get_first_available_activity()
            if activity_name == ""
            else self.__get_specified_activity(activity_name)
        )

        if activity.state == ActivityState.signed:
            return activity.name, False, "已签到该活动"
        elif activity.state == ActivityState.registered:
            return activity.name, True, "已报名该活动"
        elif activity.state == ActivityState.blocked:
            return activity.name, False, "该活动未开始"

        success, reason = self.__register_with_id(activity.id)
        return activity.name, success, reason

    def sign(self) -> tuple[tuple[str, bool, str]]:
        """Sign in each registered activity.

        Returns:
            Results of each task, structured like:
            `(("Task 1", True, "Signed in!"), ...)`
        """
        activities = self._activities.search(state=ActivityState.registered)

        results = []
        for activity in activities:
            try:
                message = self.__sign_with_id(activity.id)
            except LegymException as e:
                results.append((activity.name, False, e.message))
            else:
                results.append((activity.name, True, message))

        return tuple(results)

    def running(self, distance: str = "") -> tuple[float, bool]:
        """Upload running data.

        Args:
            distance: Running distance, default to "", in which case
            the upper limit of mileage will be uploaded.

        Returns:
            - [0] Actual uploaded distance.
            - [1] `True` on success, or `False` on failure.
        """
        try:
            distance = float(distance)
        except ValueError:
            distance = self.__limit

        cost_time = random.randint(20, 30)
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=cost_time)
        self._update_api(
            "running",
            {
                "startTime": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "totalMileage": distance,
                "avePace": cost_time * 60 / distance * 1000,
                "calorie": int(distance * random.uniform(70.0, 75.0)),
                "effectiveMileage": distance,
                "endTime": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "gpsMileage": distance,
                "paceNumber": distance * (random.randint(50, 150)),
                "paceRange": random.randint(5, 10),
            },
        )

        response = self.request("running")
        return distance, response["data"]
