from enum import Enum


class ActivityState(Enum):
    SIGNED = "已签到"
    REGISTERED = "已报名"
    AVAILABLE = "可报名"
    BLOCKED = "未开始"


class LegymActivity:
    """Legym activity, excluding useless data."""

    def __init__(self, activity: dict) -> None:
        """Parse useful data of raw activity.

        Args:
            activity: Raw activity dictionary returned by Legym API.
        """
        self.__id = activity["id"]
        self.__name = activity["name"]
        if activity["signTime"] > 0:
            self.__state = ActivityState.SIGNED
        elif activity["isRegister"] == True:
            self.__state = ActivityState.REGISTERED
        elif activity["state"] == 4:
            self.__state = ActivityState.AVAILABLE
        else:
            self.__state = ActivityState.BLOCKED

    @property
    def id(self) -> str:
        """Set activity ID as read-only."""
        return self.__id

    @property
    def code(self) -> str:
        """The last four characters of activity ID."""
        return self.__id[-4:]

    @property
    def name(self) -> str:
        """Set activity name as read-only."""
        return self.__name

    @property
    def state(self) -> str:
        """Set activity state as read-only."""
        return self.__state
