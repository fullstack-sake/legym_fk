from legym.activity import *


class LegymActivities:
    """Manager of Legym activities."""

    def __init__(self, activities: list[dict]) -> None:
        """Parse each activity."""
        self.__activities = [LegymActivity(activity) for activity in activities]

    def search(
        self,
        id: str = "",
        code: str = "",
        name: str = "",
        state: ActivityState = ActivityState.unknown,
    ) -> list[LegymActivity]:
        """Get activity by specified rule.

        Args:
            id: Activity ID, default to "".
            code: Activity code, default to "".
            name: Activity name, default to "".
            state: Activity state, default to `ActivityState.unknown`.

        Returns:
            List of Legym activities under specified rules.
        """
        results = self.__activities.copy()

        if id != "":
            results = list(filter(lambda activity: activity.id == id, results))
        if code != "":
            results = list(filter(lambda activity: activity.code == code, results))
        if name != "":
            results = list(filter(lambda activity: activity.name == name, results))
        if state != ActivityState.unknown:
            results = list(filter(lambda activity: activity.state == state, results))

        return results
