import allure
import requests

from constants import BASE_URL, ORDERS_ENDPOINT
from helpers import create_order


@allure.epic("Stellar Burgers API")
@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_with_authorization(self, token, ingredients):
        create_order(token, ingredients)
        response = requests.get(
            f"{BASE_URL}{ORDERS_ENDPOINT}",
            headers={"Authorization": token},
            timeout=20,
        )
        body = response.json()

        assert all((
            response.status_code == 200,
            body["success"] is True,
            "orders" in body,
            isinstance(body["orders"], list),
        ))

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_without_authorization(self):
        response = requests.get(f"{BASE_URL}{ORDERS_ENDPOINT}", timeout=20)

        assert (response.status_code, response.json()) == (
            401,
            {"success": False, "message": "You should be authorised"},
        )
