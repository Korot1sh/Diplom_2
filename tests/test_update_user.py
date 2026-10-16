import allure
import requests

from constants import BASE_URL, USER_ENDPOINT
from helpers import unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("Изменение данных пользователя")
class TestUpdateUser:
    @allure.title("Изменение email пользователя с авторизацией")
    def test_update_user_email_with_authorization(self, created_user):
        _, access_token = created_user
        new_email = unique_user()["email"]
        response = requests.patch(
            f"{BASE_URL}{USER_ENDPOINT}",
            headers={"Authorization": access_token},
            json={"email": new_email},
            timeout=20,
        )
        body = response.json()

        assert all((response.status_code == 200, body["success"] is True, body["user"]["email"] == new_email))

    @allure.title("Изменение password пользователя с авторизацией")
    def test_update_user_password_with_authorization(self, created_user):
        _, access_token = created_user
        new_password = unique_user()["password"]
        response = requests.patch(
            f"{BASE_URL}{USER_ENDPOINT}",
            headers={"Authorization": access_token},
            json={"password": new_password},
            timeout=20,
        )

        assert (response.status_code, response.json()["success"]) == (200, True)

    @allure.title("Изменение name пользователя с авторизацией")
    def test_update_user_name_with_authorization(self, created_user):
        _, access_token = created_user
        new_name = unique_user()["name"]
        response = requests.patch(
            f"{BASE_URL}{USER_ENDPOINT}",
            headers={"Authorization": access_token},
            json={"name": new_name},
            timeout=20,
        )
        body = response.json()

        assert all((response.status_code == 200, body["success"] is True, body["user"]["name"] == new_name))

    @allure.title("Изменение email без авторизации возвращает ошибку")
    def test_update_user_email_without_authorization(self):
        response = requests.patch(
            f"{BASE_URL}{USER_ENDPOINT}",
            json={"email": unique_user()["email"]},
            timeout=20,
        )

        assert (response.status_code, response.json()) == (
            401,
            {"success": False, "message": "You should be authorised"},
        )

    @allure.title("Изменение password без авторизации возвращает ошибку")
    def test_update_user_password_without_authorization(self):
        response = requests.patch(
            f"{BASE_URL}{USER_ENDPOINT}",
            json={"password": unique_user()["password"]},
            timeout=20,
        )

        assert (response.status_code, response.json()) == (
            401,
            {"success": False, "message": "You should be authorised"},
        )

    @allure.title("Изменение name без авторизации возвращает ошибку")
    def test_update_user_name_without_authorization(self):
        response = requests.patch(
            f"{BASE_URL}{USER_ENDPOINT}",
            json={"name": unique_user()["name"]},
            timeout=20,
        )

        assert (response.status_code, response.json()) == (
            401,
            {"success": False, "message": "You should be authorised"},
        )
