import sys

from legym import LegymHacker


def parse_args():
    try:
        username = sys.argv[1]
    except IndexError:
        raise IndexError("username not provided") from None

    try:
        password = sys.argv[2]
    except IndexError:
        raise IndexError("password not provided") from None

    try:
        distance = float(sys.argv[3])
    except IndexError:
        distance = 0
    except ValueError:
        raise ValueError("invalid distance")

    try:
        activity = sys.argv[4]
    except IndexError:
        activity = ""

    return username, password, distance, activity


if __name__ == "__main__":
    username, password, distance, activity = parse_args()
    hacker = LegymHacker()
    hacker.login(username, password)
    hacker.running(distance)
    hacker.sign_up(activity)
    hacker.sign_in()
