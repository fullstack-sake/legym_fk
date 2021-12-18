from enum import IntEnum


class ActivityState(IntEnum):
    unknown = 0
    signed = 1
    registered = 2
    available = 3
    blocked = 4


class LegymActivity:
    """Legym activity, excluding useless data."""

    def __init__(self, activity: dict) -> None:
        """Parse useful data of raw activity.

        Args:
            activity: Raw activity dictionary returned by Legym API.
        """
        self.__id = activity["id"]
        self.__name = activity["name"]
        if activity["signTime"] != None:
            self.__state = ActivityState.signed
        elif activity["isRegister"] == True:
            self.__state = ActivityState.registered
        elif activity["state"] == 4:
            self.__state = ActivityState.available
        elif activity["state"] == 0:
            self.__state = ActivityState.blocked
        else:
            self.__state = ActivityState.unknown

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
