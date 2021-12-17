import random
from datetime import datetime, timedelta

from legym.request import LegymRequester


class ActivityState:
    """Current state of activity, concerning availability and user actions."""

    # Already signed in.
    signed = 0
    # Already signed up, but not signed in yet.
    registered = 1
    # Open for signing up.
    available = 2
    # Unavailable to user.
    blocked = 3


class LegymHacker(LegymRequester):
    """Legym hacker application."""

    def __init__(self) -> None:
        super().__init__()

    def __get_semester(self) -> None:
        """Get semester ID and update concerning API."""
        response = self._request("semester")
        semester_id = response.get("id")
        self._update_api("limit", {"semesterId": semester_id})
        self._update_api("running", {"semesterId": semester_id})

    def __get_limit(self) -> float:
        """Get mileage limit and update concerning API.

        Returns:
            Upper limit of mileage.
        """
        response = self._request("limit")
        limit_id = response.get("limitationsGoalsSexInfoId")
        self._update_api("running", {"limitationsGoalsSexInfoId": limit_id})
        return response.get("effectiveMileageEnd")

    def __get_activities(self) -> None:
        """Get activities open for signing up."""
        response = self._request("activities")
        activities_list = response.get("items")

        self.__activities = []
        for activity in activities_list:
            if activity["signTime"]:
                self.__activities.append(
                    {
                        "id": activity["id"],
                        "name": activity["name"],
                        "state": ActivityState.signed,
                    }
                )
            elif activity["isRegister"]:
                self.__activities.append(
                    {
                        "id": activity["id"],
                        "name": activity["name"],
                        "state": ActivityState.registered,
                    }
                )
            elif activity["state"] == 4:
                self.__activities.append(
                    {
                        "id": activity["id"],
                        "name": activity["name"],
                        "state": ActivityState.available,
                    }
                )
            else:
                self.__activities.append(
                    {
                        "id": activity["id"],
                        "name": activity["name"],
                        "state": ActivityState.blocked,
                    }
                )

        self.__activities.sort(key=lambda activity: activity["state"])

    def __get_first_available_activity(self) -> dict:
        """Get first available activity.

        Returns:
            Activity data.
        """
        try:
            return list(
                filter(
                    lambda dic: dic["state"] == ActivityState.available,
                    self.__activities,
                )
            )[0]
        except IndexError:
            raise IndexError("available activity not found")

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
                    lambda dic: dic["name"].find(activity_name) != -1, self.__activities
                )
            )[0]
        except IndexError:
            raise IndexError(f"activity '{activity_name}' not found")

    def __sign_up_with_id(self, activity_id: str) -> dict:
        """Sign up activity with ID.

        Args:
            activity_id: ID of activity.

        Returns:
            Response data.
        """
        self._update_api("signUp", {"activityId": activity_id})
        response = self._request("signUp")
        return response.data

    def __sign_in_with_id(self, activity_id: str) -> str:
        """Sign in activity with ID.

        Args:
            activity_id: ID of activity.

        Returns:
            Response message.
        """
        self._update_api("signIn", {"activityId": activity_id})
        response = self._request("signIn")
        return response.message

    def login(self, username: str, password: str) -> dict:
        """Log in Legym account.

        Args:
            username: Legym username.
            password: Legym password.

        Returns:
            User's personal info.
        """
        self._update_api("login", {"userName": username, "password": password})
        response = self._request("login")

        self._headers.update(
            {
                "authorization": f"Bearer {response.get('accessToken')}",
                "Organization": response.get("schoolId"),
            }
        )
        self._update_api("signIn", {"userId": response.get("id")})
        self.__get_semester()
        self.__get_activities()
        self.__limit = self.__get_limit()

        return {
            "name": response.get("realName"),
            "school": response.get("schoolName"),
        }

    def sign_up(self, activity_name: str = "") -> dict:
        """Sign up for activity.

        Args:
            activity_name: Name of activity to sign up for,
            default to "", in which case the first available
            activity will be selected.

        Returns:
            Response data, containing key `success` and `reason`.
        """
        activity = (
            self.__get_first_available_activity()
            if not activity_name
            else self.__get_specified_activity(activity_name)
        )

        if activity["state"] == ActivityState.signed:
            return {"success": False, "reason": "signed in already"}
        elif activity["state"] == ActivityState.registered:
            return {"success": True, "reason": "signed up already"}
        elif activity["state"] == ActivityState.blocked:
            return {"success": False, "reason": "not available yet"}

        return self.__sign_up_with_id(activity["id"])

    def sign_in(self) -> dict[str, bool]:
        """Sign in each registered activity.

        Returns:
            Result of each task, structured like: `{"Task1": True}`
        """
        registered_activities = list(
            filter(
                lambda dic: dic["state"] == ActivityState.registered,
                self.__activities,
            )
        )

        results = {}
        for activity in registered_activities:
            try:
                self.__sign_in_with_id(activity["id"])
            except Exception:
                results[activity["name"]] = False
                continue
            else:
                results[activity["name"]] = True

        return results

    def running(self, distance: float = 0) -> bool:
        """Upload running data.

        Args:
            distance: Running distance, default to 0, in which case
            the upper limit of mileage will be uploaded.

        Returns:
            `True` on success, or `False` on failure.
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

        response = self._request("running")
        return response.data
