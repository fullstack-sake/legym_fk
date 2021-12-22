import sys

import legym


def automation_for_debug():
    if len(sys.argv) != 2:
        raise Exception("arguments not provided")
    username, password, distance, activity = sys.argv[1].split("#")

    user = legym.login(username, password)
    print(f"{user=}")

    running_result = user.running(float(distance))
    print(f"{running_result=}")

    register_result = user.register(name=activity)
    print(f"{register_result=}")

    sign_result = user.sign()
    print(f"{sign_result=}")


def automation_for_workflow():
    if len(sys.argv) != 2:
        raise Exception("arguments not provided")
    username, password, distance, activity = sys.argv[1].split("#")

    print("Login...", end="")
    user = legym.login(username, password)
    print("success")

    print("Running...", end="")
    actual_distance, success = user.running(float(distance))
    if success:
        print(f"{actual_distance} km")
    else:
        print("failed")

    print("Registering...", end="")
    _, success, _ = user.register(name=activity)
    if success:
        print("success")
    else:
        print("failed")

    print("Signing...", end="")
    results = user.sign()
    for result in results:
        if result[1]:
            print("success")
        else:
            print("failed")


if __name__ == "__main__":
    automation_for_workflow()
