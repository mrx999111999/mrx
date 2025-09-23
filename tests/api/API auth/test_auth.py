import pytest
from api.api_manager import ApiManager
from typing import Any


class TestAuth:
    @pytest.mark.api
    @pytest.mark.smoke
    def test_register_user(self, api_manager: ApiManager, test_user: dict[str, Any]) -> None:
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        # Проверки
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    @pytest.mark.api
    @pytest.mark.smoke
    def test_login_user(self, api_manager: ApiManager, registered_user: dict[str, Any]) -> None:
        """
        Тест на авторизацию пользователя.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    @pytest.mark.api
    @pytest.mark.regression
    def test_login_with_invalid_email(self, api_manager: ApiManager, test_user: dict[str, Any]) -> None:
        """
        Тест на авторизацию пользователя c неверным email.
        """
        login_data_with_invalid_email = {
            "email": "0000000@gmail.com",
            "password": test_user["password"]
        }
        api_manager.auth_api.login_user(login_data_with_invalid_email, 401)

    @pytest.mark.api
    @pytest.mark.regression
    def test_login_with_invalid_password(self, api_manager: ApiManager, test_user: dict[str, Any]) -> None:
        """
        Тест на авторизацию пользователя c неверным паролем.
        """
        login_data_with_invalid_password = {
            "email": test_user["email"],
            "password": "1000"
        }
        api_manager.auth_api.login_user(login_data_with_invalid_password, 401)

    @pytest.mark.api
    @pytest.mark.regression
    def test_login_with_empty_body(self, api_manager: ApiManager, test_user: dict[str, Any]) -> None:
        """
        Тест на авторизацию пользователя c пустым телом.
        """
        api_manager.auth_api.login_user({}, 401)
