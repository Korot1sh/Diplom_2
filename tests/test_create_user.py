import allure
import pytest
import requests

from tests.conftest import BASE_URL, REGISTER_ENDPOINT, unique_user, register_user


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        user = unique_user()

        access_token = None
        try:
            with allure.step("Создать уникального пользователя"):
                response = register_user(user)

            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert body["user"]["email"] == user["email"]
            assert body["user"]["name"] == user["name"]
            assert body["accessToken"]
            assert body["refreshToken"]
            access_token = body["accessToken"]
        finally:
            if access_token:
                delete_response = requests.delete(
                    f"{BASE_URL}/api/auth/user",
                    headers={"Authorization": access_token},
                    timeout=20,
                )
                assert delete_response.status_code in (200, 202), delete_response.text

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user(self, created_user):
        user, _ = created_user

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
