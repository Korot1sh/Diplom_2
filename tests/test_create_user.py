import allure
import pytest
import requests

from tests.constants import BASE_URL, REGISTER_ENDPOINT
from tests.helpers import register_user, unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, users_to_delete):
        user = unique_user()

        with allure.step("Создать уникального пользователя"):
            response = register_user(user)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == user["email"]
        assert body["user"]["name"] == user["name"]
        assert body["accessToken"]
        assert body["refreshToken"]

        users_to_delete.append(body["accessToken"])

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user(self, created_user):
        user, _, registration_response = created_user

        assert registration_response.status_code == 200

        with allure.step("Повторно зарегистрировать пользователя"):
            response = register_user(user)

        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "User already exists",
        }

    @pytest.mark.parametrize(
        "missing_field",
        ["email", "password", "name"],
        ids=["без_email", "без_password", "без_name"],
    )
    @allure.title("Создание пользователя без обязательного поля")
    def test_create_user_without_required_field(self, missing_field):
        user = unique_user()
        user.pop(missing_field)

        with allure.step(f"Создать пользователя без поля {missing_field}"):
            response = requests.post(
                f"{BASE_URL}{REGISTER_ENDPOINT}",
                json=user,
                timeout=20,
            )

        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "Email, password and name are required fields",
        }
