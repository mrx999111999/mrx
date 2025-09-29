import pytest
from typing import Any

from enums.roles import Roles
from models.test_user import UserRegisterRequest, UserRegisterResponse
from api.api_manager import ApiManager


class TestAuth:
    @pytest.mark.api
    @pytest.mark.smoke
    def test_register_user(self, api_manager: ApiManager, test_user: UserRegisterRequest) -> None:
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = UserRegisterResponse(**response.json())

        # Проверки
        assert response_data.email == test_user.email, "Email не совпадает"
        assert Roles.USER in response_data.roles, "Роль USER должна быть у пользователя"

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
        response = api_manager.auth_api.login_user(login_data).json()

        # Проверки
        assert "accessToken" in response, "Токен доступа отсутствует в ответе"
        assert response["user"]["email"] == registered_user["email"], "Email не совпадает"

    @pytest.mark.api
    @pytest.mark.regression
    def test_login_with_invalid_email(self, api_manager: ApiManager, registered_user: dict[str, Any]) -> None:
        """
        Тест на авторизацию пользователя c неверным email.
        """
        login_data_with_invalid_email = {
            "email": "0000000@gmail.com",
            "password": registered_user["password"]
        }
        api_manager.auth_api.login_user(login_data_with_invalid_email, 401)

    @pytest.mark.api
    @pytest.mark.regression
    def test_login_with_invalid_password(self, api_manager: ApiManager, registered_user: dict[str, Any]) -> None:
        """
        Тест на авторизацию пользователя c неверным паролем.
        """
        login_data_with_invalid_password = {
            "email": registered_user["email"],
            "password": "1000"
        }
        api_manager.auth_api.login_user(login_data_with_invalid_password, 401)

    @pytest.mark.api
    @pytest.mark.regression
    def test_login_with_empty_body(self, api_manager: ApiManager) -> None:
        """
        Тест на авторизацию пользователя c пустым телом.
        """
        api_manager.auth_api.login_user({}, 401)
