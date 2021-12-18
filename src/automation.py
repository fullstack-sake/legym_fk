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
    print("Initialized")

    hacker.login(username, password)
    print("Login success")

    success = hacker.running(distance)
    if success:
        print(f"Running data uploaded: {distance}km")
    else:
        print("Running data upload failed.")

    success, reason = hacker.sign_up(activity)
    if success:
        print("Sign up success")
    else:
        print(reason)

    task_result = [item[1] for item in hacker.sign_in()]
    if all(task_result):
        print("All activities signed in")
    elif any(task_result):
        print("Signed in part of activities signed up")
    else:
        print("No activity signed in")
