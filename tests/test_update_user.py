import allure
import requests

from tests.constants import BASE_URL, LOGIN_ENDPOINT, USER_ENDPOINT
from tests.helpers import unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("Изменение данных пользователя")
class TestUpdateUser:
    @allure.title("Изменение email пользователя с авторизацией")
    def test_update_user_email_with_authorization(self, created_user):
        user, access_token, registration_response = created_user
        assert registration_response.status_code == 200

        new_email = unique_user()["email"]

        with allure.step("Изменить email с токеном"):
            response = requests.patch(
                f"{BASE_URL}{USER_ENDPOINT}",
                headers={"Authorization": access_token},
                json={"email": new_email},
                timeout=20,
            )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == new_email

    @allure.title("Изменение password пользователя с авторизацией")
    def test_update_user_password_with_authorization(self, created_user):
        user, access_token, registration_response = created_user
        assert registration_response.status_code == 200

        new_password = unique_user()["password"]

        with allure.step("Изменить password с токеном"):
            response = requests.patch(
                f"{BASE_URL}{USER_ENDPOINT}",
                headers={"Authorization": access_token},
                json={"password": new_password},
                timeout=20,
            )

        assert response.status_code == 200
        assert response.json()["success"] is True

        login_response = requests.post(
            f"{BASE_URL}{LOGIN_ENDPOINT}",
            json={"email": user["email"], "password": new_password},
            timeout=20,
        )

        assert login_response.status_code == 200
        assert login_response.json()["success"] is True

    @allure.title("Изменение name пользователя с авторизацией")
    def test_update_user_name_with_authorization(self, created_user):
        _, access_token, registration_response = created_user
        assert registration_response.status_code == 200

        new_name = unique_user()["name"]

        with allure.step("Изменить name с токеном"):
            response = requests.patch(
                f"{BASE_URL}{USER_ENDPOINT}",
                headers={"Authorization": access_token},
                json={"name": new_name},
                timeout=20,
            )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["name"] == new_name

    @allure.title("Изменение email без авторизации возвращает ошибку")
    def test_update_user_email_without_authorization(self):
        response = requests.patch(
            f"{BASE_URL}{USER_ENDPOINT}",
            json={"email": unique_user()["email"]},
            timeout=20,
        )

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised",
        }

    @allure.title("Изменение password без авторизации возвращает ошибку")
    def test_update_user_password_without_authorization(self):
        response = requests.patch(
            f"{BASE_URL}{USER_ENDPOINT}",
            json={"password": unique_user()["password"]},
            timeout=20,
        )

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised",
        }

    @allure.title("Изменение name без авторизации возвращает ошибку")
    def test_update_user_name_without_authorization(self):
        response = requests.patch(
            f"{BASE_URL}{USER_ENDPOINT}",
            json={"name": unique_user()["name"]},
            timeout=20,
        )

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised",
        }
