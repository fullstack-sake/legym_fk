import random
from datetime import datetime, timedelta

from legym.exception import LegymException
from legym.requester import LegymRequester


class ActivityState:
    """Current state of activity, concerning availability and user actions."""

    # Already signed in.
    SIGNED = 0
    # Already signed up, but not signed in yet.
    REGISTERED = 1
    # Open for signing up.
    AVAILABLE = 2
    # Unavailable to user.
    BLOCKED = 3


class LegymHacker(LegymRequester):
    """Legym hacker application."""

    def __init__(self) -> None:
        super().__init__()

    def __get_semester(self) -> None:
        """Get semester ID and update relevant API."""
        response = self.request("semester")
        semester_id = response["id"]
        self._update_api("limit", {"semesterId": semester_id})
        self._update_api("running", {"semesterId": semester_id})

    def __get_limit(self) -> float:
        """Get mileage limit and update relevant API.

        Returns:
            Upper limit of mileage.
        """
        response = self.request("limit")
        limit_id = response["limitationsGoalsSexInfoId"]
        self._update_api("running", {"limitationsGoalsSexInfoId": limit_id})
        return response["effectiveMileageEnd"]

    def __get_activities(self) -> None:
        """Get activities open for signing up."""
        response = self.request("activities")
        activities_list = response["items"]

        self._activities = []
        for activity in activities_list:
            if activity["signTime"]:
                self._activities.append(
                    {
                        "id": activity["id"],
                        "name": activity["name"],
                        "state": ActivityState.SIGNED,
                    }
                )
            elif activity["isRegister"]:
                self._activities.append(
                    {
                        "id": activity["id"],
                        "name": activity["name"],
                        "state": ActivityState.REGISTERED,
                    }
                )
            elif activity["state"] == 4:
                self._activities.append(
                    {
                        "id": activity["id"],
                        "name": activity["name"],
                        "state": ActivityState.AVAILABLE,
                    }
                )
            else:
                self._activities.append(
                    {
                        "id": activity["id"],
                        "name": activity["name"],
                        "state": ActivityState.BLOCKED,
                    }
                )

        self._activities.sort(key=lambda activity: activity["state"])

    def __get_first_available_activity(self) -> dict:
        """Get first available activity.

        Returns:
            Activity data.
        """
        try:
            return list(
                filter(
                    lambda dic: dic["state"] == ActivityState.AVAILABLE,
                    self._activities,
                )
            )[0]
        except IndexError:
            raise LegymException("当前没有可报名的活动")

    def __get_specified_activity(self, activity_name: str) -> dict:
        """Get specified activity.

        Args:
            activity_name: Name of specified activity.

        Returns:
            Activity data.
        """
        try:
            return list(
                filter(
                    lambda dic: dic["name"].find(activity_name) != -1, self._activities
                )
            )[0]
        except IndexError:
            raise LegymException(f"找不到活动：{activity_name}")

    def __sign_up_with_id(self, activity_id: str) -> tuple[bool, str]:
        """Sign up activity with ID.

        Args:
            activity_id: ID of activity.

        Returns:
            - [0] `True` on success, or `False` on failure.
            - [1] Reason of success or failure.
        """
        self._update_api("signUp", {"activityId": activity_id})
        response = self.request("signUp")
        return response["success"], response["reason"]

    def __sign_in_with_id(self, activity_id: str) -> str:
        """Sign in activity with ID.

        Args:
            activity_id: ID of activity.

        Returns:
            Response message.
        """
        self._update_api("signIn", {"activityId": activity_id})
        response = self.request("signIn")
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
        self._update_api("signIn", {"userId": response["id"]})
        self.__get_semester()
        self.__get_activities()
        self.__limit = self.__get_limit()

        return response["realName"], response["schoolName"]

    def sign_up(self, activity_name: str = "") -> tuple[str, bool, str]:
        """Sign up for activity.

        Args:
            activity_name: Name of activity to sign up for,
            default to "", in which case the first available
            activity will be selected.

        Returns:
            - [0] Actual signed-up activity name.
            - [1] `True` on success, or `False` on failure.
            - [2] Reason of success or failure.
        """
        activity = (
            self.__get_first_available_activity()
            if not activity_name
            else self.__get_specified_activity(activity_name)
        )

        if activity["state"] == ActivityState.SIGNED:
            return activity["name"], False, "已签到该活动"
        elif activity["state"] == ActivityState.REGISTERED:
            return activity["name"], True, "已报名该活动"
        elif activity["state"] == ActivityState.BLOCKED:
            return activity["name"], False, "该活动未开始"

        success, reason = self.__sign_up_with_id(activity["id"])
        return activity["name"], success, reason

    def sign_in(self) -> dict[str, bool]:
        """Sign in each registered activity.

        Returns:
            Result of each task, structured like: `{"Task1": True}`
        """
        registered_activities = list(
            filter(
                lambda dic: dic["state"] == ActivityState.REGISTERED,
                self._activities,
            )
        )

        results = {}
        for activity in registered_activities:
            try:
                message = self.__sign_in_with_id(activity["id"])
            except LegymException as e:
                results[activity["name"]] = e
            else:
                results[activity["name"]] = message

        return results

    def running(self, distance: float = 0) -> tuple[float, bool]:
        """Upload running data.

        Args:
            distance: Running distance, default to 0, in which case
            the upper limit of mileage will be uploaded.

        Returns:
            - [0] Actual uploaded distance.
            - [1] `True` on success, or `False` on failure.
        """
        distance = self.__limit if distance == 0 else distance
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
