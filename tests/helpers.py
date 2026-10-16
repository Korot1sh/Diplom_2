from uuid import uuid4

import requests

from constants import BASE_URL, LOGIN_ENDPOINT, ORDERS_ENDPOINT, REGISTER_ENDPOINT, USER_ENDPOINT


def unique_user():
    suffix = uuid4().hex
    return {
        "email": f"test_{suffix}@example.com",
        "password": f"Password_{suffix}",
        "name": f"Test User {suffix}",
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
        json={"email": user["email"], "password": user["password"]},
        timeout=20,
    )


def delete_user(access_token):
    return requests.delete(
        f"{BASE_URL}{USER_ENDPOINT}",
        headers={"Authorization": access_token},
        timeout=20,
    )


def create_order(access_token, ingredients):
    return requests.post(
        f"{BASE_URL}{ORDERS_ENDPOINT}",
        headers={"Authorization": access_token},
        json={"ingredients": [item["_id"] for item in ingredients]},
        timeout=20,
    )
