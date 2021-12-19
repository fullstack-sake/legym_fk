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
        distance = ""

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

    actual_distance, success = hacker.running(distance)
    if success:
        print(f"Running data uploaded: {actual_distance}km")
    else:
        print("Running data upload failed.")

    _, success, _ = hacker.register(activity)
    if success:
        print("Register success.")
    else:
        print("Register failed.")

    task_results = [item[1] for item in hacker.sign().items()]
    if all(task_results):
        print("All activities signed in")
    elif any(task_results):
        print("Signed in part of activities signed up")
    else:
        print("No activity signed in")
