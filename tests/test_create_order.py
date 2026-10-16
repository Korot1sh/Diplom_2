import allure
import requests

from constants import BASE_URL, ORDERS_ENDPOINT
from helpers import create_order


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_with_authorization(self, token, ingredients):
        response = create_order(token, ingredients)
        body = response.json()

        assert all((response.status_code == 200, body["success"] is True, bool(body["order"]["number"])))

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_authorization(self, ingredients):
        response = requests.post(
            f"{BASE_URL}{ORDERS_ENDPOINT}",
            json={"ingredients": [item["_id"] for item in ingredients]},
            timeout=20,
        )

        assert (response.status_code, response.json()) == (
            401,
            {"success": False, "message": "You should be authorised"},
        )
