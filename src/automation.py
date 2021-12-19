import sys

from legym import Legym


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
    hacker = Legym(username, password)
    print("Login success")

    actual_distance, success = hacker.running(distance)
    if success:
        print(f"Running data uploaded: {actual_distance} km")
    else:
        print("Running data upload failed.")

    _, success, _ = hacker.register(activity)
    if success:
        print("Register success.")
    else:
        print("Register failed.")

    task_results = [result[1] for result in hacker.sign()]
    if all(task_results):
        print("All activities signed in")
    elif any(task_results):
        print("Signed in part of activities")
    else:
        print("No activity signed in")
