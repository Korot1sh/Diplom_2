import allure
import pytest
import requests

from tests.conftest import BASE_URL, USER_ENDPOINT, unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("Изменение данных пользователя")
class TestUpdateUser:
    @pytest.mark.parametrize(
        "field",
        ["email", "password", "name"],
        ids=["email", "password", "name"],
    )
    @allure.title("Изменение поля пользователя с авторизацией")
    def test_update_user_field_with_authorization(self, created_user, field):
        user, access_token = created_user
        updated_user = unique_user()
        new_value = updated_user[field]

        payload = {field: new_value}

        with allure.step(f"Изменить поле {field} с токеном"):
            response = requests.patch(
                f"{BASE_URL}{USER_ENDPOINT}",
                headers={"Authorization": access_token},
                json=payload,
                timeout=20,
            )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True

        if field == "password":
            login_response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json={"email": user["email"], "password": new_value},
                timeout=20,
            )
            assert login_response.status_code == 200
            assert login_response.json()["success"] is True
        else:
            assert body["user"][field] == new_value

        user[field] = new_value

    @pytest.mark.parametrize(
        "field",
        ["email", "password", "name"],
        ids=["email", "password", "name"],
    )
    @allure.title("Изменение поля пользователя без авторизации возвращает ошибку")
    def test_update_user_field_without_authorization(self, field):
        user = unique_user()
        payload = {field: user[field]}

        with allure.step(f"Изменить поле {field} без токена"):
            response = requests.patch(
                f"{BASE_URL}{USER_ENDPOINT}",
                json=payload,
                timeout=20,
            )

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised",
        }
