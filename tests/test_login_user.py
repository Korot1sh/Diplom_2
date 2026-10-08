import allure
import requests

from tests.conftest import BASE_URL, LOGIN_ENDPOINT


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestLoginUser:
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, created_user):
        user, _ = created_user

        with allure.step("Авторизоваться существующими данными"):
            response = requests.post(
                f"{BASE_URL}{LOGIN_ENDPOINT}",
                json={
                    "email": user["email"],
                    "password": user["password"],
                },
                timeout=20,
            )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == user["email"]
        assert body["user"]["name"] == user["name"]
        assert body["accessToken"]
        assert body["refreshToken"]

    @allure.title("Логин с неверным логином и паролем")
    def test_login_with_invalid_credentials(self, created_user):
        user, _ = created_user

        with allure.step("Отправить неверные email и password"):
            response = requests.post(
                f"{BASE_URL}{LOGIN_ENDPOINT}",
                json={
                    "email": f"wrong_{user['email']}",
                    "password": "WrongPassword",
                },
                timeout=20,
            )

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "email or password are incorrect",
        }
