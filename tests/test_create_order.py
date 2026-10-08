import allure
import requests

BASE_URL = "https://qa-stellarburgers.education-services.ru"


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Авторизованный пользователь может создать заказ с ингредиентами")
    def test_create_order_authorized(self, token, ingredients):
        response = requests.post(
            f"{BASE_URL}/api/orders",
            headers={"Authorization": token},
            json={"ingredients": ingredients},
            timeout=20,
        )

        assert response.status_code == 200

        body = response.json()
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Неавторизованный пользователь может создать заказ")
    def test_create_order_without_authorization(self, ingredients):
        response = requests.post(
            f"{BASE_URL}/api/orders",
            json={"ingredients": ingredients},
            timeout=20,
        )

        assert response.status_code == 200

        body = response.json()
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Можно создать заказ без ингредиентов")
    def test_create_order_without_ingredients(self, token):
        response = requests.post(
            f"{BASE_URL}/api/orders",
            headers={"Authorization": token},
            json={"ingredients": []},
            timeout=20,
        )

        assert response.status_code == 400

        body = response.json()
        assert body["success"] is False
        assert body["message"] == "Ingredient ids must be provided"

    @allure.title("Нельзя создать заказ с неверным хешем ингредиента")
    def test_create_order_invalid_ingredient_hash(self, token):
        response = requests.post(
            f"{BASE_URL}/api/orders",
            headers={"Authorization": token},
            json={
                "ingredients": [
                    "invalid_ingredient_hash"
                ]
            },
            timeout=20,
        )

        assert response.status_code == 500
        assert "Internal Server Error" in response.text
