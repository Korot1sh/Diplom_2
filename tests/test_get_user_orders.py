import allure
import requests

from tests.conftest import BASE_URL


ORDERS_ENDPOINT = "/api/orders"


@allure.epic("Stellar Burgers API")
@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_with_authorization(self, created_user, ingredients):
        _, access_token = created_user

        order_response = requests.post(
            f"{BASE_URL}{ORDERS_ENDPOINT}",
            headers={"Authorization": access_token},
            json={"ingredients": ingredients},
            timeout=20,
        )
        assert order_response.status_code == 200

        response = requests.get(
            f"{BASE_URL}{ORDERS_ENDPOINT}",
            headers={"Authorization": access_token},
            timeout=20,
        )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "orders" in body
        assert isinstance(body["orders"], list)

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_without_authorization(self):
        response = requests.get(
            f"{BASE_URL}{ORDERS_ENDPOINT}",
            timeout=20,
        )

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised",
        }
