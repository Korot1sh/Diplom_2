import allure
import pytest
import requests

from tests.constants import BASE_URL, INGREDIENTS_ENDPOINT
from tests.helpers import delete_user, register_user, unique_user


@pytest.fixture
def created_user():
    user = unique_user()
    response = register_user(user)
    body = response.json()
    access_token = body.get("accessToken")

    yield user, access_token, response

    if access_token:
        with allure.step("Удалить тестового пользователя"):
            delete_user(access_token)


@pytest.fixture
def token(created_user):
    _, access_token, _ = created_user
    return access_token


@pytest.fixture
def ingredients():
    response = requests.get(
        f"{BASE_URL}{INGREDIENTS_ENDPOINT}",
        timeout=20,
    )
    return response.json()["data"][:2]


@pytest.fixture
def users_to_delete():
    access_tokens = []
    yield access_tokens

    for access_token in access_tokens:
        with allure.step("Удалить тестового пользователя"):
            delete_user(access_token)
