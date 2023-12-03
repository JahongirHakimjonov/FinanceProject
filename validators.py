from exceptions import BadRequestException


def check_username_unique(users: list, username: str) -> bool:
    for user in users:
        if user["username"] == username:
            raise BadRequestException(f"{username} is already taken")
    return True


def check_user_exists(users: list, user_id: str) -> int:
    for user in users:
        if user["id"] == user_id:
            return 200

    return 404
