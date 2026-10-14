import uuid

import requests

from tests.constants import (
    BASE_URL,
    LOGIN_ENDPOINT,
    REGISTER_ENDPOINT,
    USER_ENDPOINT,
)


def unique_user():
    suffix = uuid.uuid4().hex
    return {
        "email": f"api_test_{suffix}@example.com",
        "password": f"TestPassword_{suffix}",
        "name": f"Api Test {suffix}",
    }


def register_user(user):
    return requests.post(
        f"{BASE_URL}{REGISTER_ENDPOINT}",
        json=user,
        timeout=20,
    )


def login_user(user):
    return requests.post(
        f"{BASE_URL}{LOGIN_ENDPOINT}",
        json={
            "email": user["email"],
            "password": user["password"],
        },
        timeout=20,
    )


def delete_user(access_token):
    return requests.delete(
        f"{BASE_URL}{USER_ENDPOINT}",
        headers={"Authorization": access_token},
        timeout=20,
    )
