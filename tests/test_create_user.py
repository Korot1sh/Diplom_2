import allure
import requests

from constants import BASE_URL, REGISTER_ENDPOINT
from helpers import register_user, unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, users_to_delete):
        user = unique_user()
        response = register_user(user)
        body = response.json()
        access_token = body["accessToken"]
        users_to_delete.append(access_token)

        assert all((
            response.status_code == 200,
            body["success"] is True,
            body["user"]["email"] == user["email"],
            body["user"]["name"] == user["name"],
            bool(body["accessToken"]),
            bool(body["refreshToken"]),
        ))

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user(self, created_user):
        user, _ = created_user
        response = register_user(user)

        assert (response.status_code, response.json()) == (
            403,
            {"success": False, "message": "User already exists"},
        )

    @allure.title("Создание пользователя без email")
    def test_create_user_without_email(self):
        user = unique_user()
        user.pop("email")
        response = requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=user, timeout=20)

        assert (response.status_code, response.json()) == (
            403,
            {"success": False, "message": "Email, password and name are required fields"},
        )

    @allure.title("Создание пользователя без password")
    def test_create_user_without_password(self):
        user = unique_user()
        user.pop("password")
        response = requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=user, timeout=20)

        assert (response.status_code, response.json()) == (
            403,
            {"success": False, "message": "Email, password and name are required fields"},
        )

    @allure.title("Создание пользователя без name")
    def test_create_user_without_name(self):
        user = unique_user()
        user.pop("name")
        response = requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=user, timeout=20)

        assert (response.status_code, response.json()) == (
            403,
            {"success": False, "message": "Email, password and name are required fields"},
        )
