import allure
import requests

from constants import BASE_URL, LOGIN_ENDPOINT
from helpers import login_user


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestLoginUser:
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, created_user):
        user, _ = created_user
        response = login_user(user)
        body = response.json()

        assert all((
            response.status_code == 200,
            body["success"] is True,
            body["user"]["email"] == user["email"],
            body["user"]["name"] == user["name"],
            bool(body["accessToken"]),
            bool(body["refreshToken"]),
        ))

    @allure.title("Логин с неверным логином и паролем")
    def test_login_with_invalid_credentials(self, created_user):
        user, _ = created_user
        response = requests.post(
            f"{BASE_URL}{LOGIN_ENDPOINT}",
            json={"email": f"wrong_{user['email']}", "password": "WrongPassword"},
            timeout=20,
        )

        assert (response.status_code, response.json()) == (
            401,
            {"success": False, "message": "email or password are incorrect"},
        )
