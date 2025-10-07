import allure
import pytest

from pytest_check import check

from db_requester.db_helpers import DBHelper
from enums.roles import Roles
from models.models import UserRegisterRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse
from api.api_manager import ApiManager


@pytest.mark.api
@allure.epic("Auth API")
@allure.feature("Авторизация")
class TestAuth:
    @pytest.mark.smoke
    @allure.story("Успешная регистрация нового пользователя")
    @allure.title("Регистрация пользователя с валидными данными")
    @allure.tag("smoke", "api", "registration")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_register_user(self, api_manager: ApiManager, test_user: UserRegisterRequest, db_helper: DBHelper) -> None:
        """
        Тест на регистрацию пользователя.
        """
        with allure.step("Регистрация пользователя через API"):
            response = api_manager.auth_api.register_user(test_user).json()
            response_data = UserRegisterResponse(**response)

        with allure.step("Получение данных пользователя из БД"):
            db_user = db_helper.get_user_by_id(response_data.id)

        with allure.step("Проверки API ответа"):
            with check:
                assert response_data.email == test_user.email, "Email не совпадает"
                assert Roles.USER.value in response_data.roles, "Роль USER должна быть у пользователя"

        with allure.step("Проверки в БД"):
            with check:
                assert db_user is not None, "Пользователь не найден в БД"
                assert db_user.id == response_data.id, "id в БД не совпадает"
                assert db_user.email == test_user.email, "email в БД не совпадает"
                assert db_user.full_name == test_user.fullName, "fullName в БД не совпадает"
                assert db_user.password != test_user.password, "Пароль должен быть захэширован"
                assert db_user.verified == True, "Пользователь должен быть верифицирован"
                assert db_user.banned == False, "Пользователь не должен быть забанен"
                assert Roles.USER.value in db_user.roles, "Роль USER должна быть в БД"
                assert db_user.created_at is not None, "Дата создания должна быть заполнена"
                assert db_user.updated_at is not None, "Дата обновления должна быть заполнена"

    @pytest.mark.smoke
    @allure.story("Успешная авторизация пользователя")
    @allure.title("Логин пользователя с валидными данными")
    @allure.tag("smoke", "api", "login")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_user(self, api_manager: ApiManager, registered_user: UserRegisterResponse,
                        test_user: UserRegisterRequest) -> None:
        """
        Тест на авторизацию пользователя.
        """
        with allure.step("Подготовка данных для логина"):
            login_data = UserLoginRequest(
                email=registered_user.email,
                password=test_user.password
            )

        with allure.step("Авторизация пользователя через API"):
            response = api_manager.auth_api.login_user(login_data).json()
            response_data = UserLoginResponse(**response)

        with allure.step("Проверки API ответа"):
            with check:
                assert response_data.user["id"] == registered_user.id, "id не совпадает"
                assert response_data.user["email"] == registered_user.email, "email не совпадает"
                assert response_data.user["fullName"] == registered_user.fullName, "fullName не совпадает"
                assert response_data.user["roles"] == registered_user.roles, "roles не совпадает"

    @pytest.mark.regression
    @allure.story("Неуспешная авторизация с невалидными данными")
    @allure.title("Логин с неверным email")
    @allure.tag("regression", "api", "login", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_invalid_email(self, api_manager: ApiManager, registered_user: UserRegisterResponse,
                                      test_user: UserRegisterRequest) -> None:
        """
        Тест на авторизацию пользователя c неверным email.
        """
        with allure.step("Подготовка данных с невалидным email"):
            login_data_with_invalid_email = {
                "email": "0000000@gmail.com",
                "password": test_user.password
            }

        with allure.step("Попытка авторизации пользователя с невалидным email"):
            api_manager.auth_api.login_user(login_data_with_invalid_email, 401)

    @pytest.mark.regression
    @allure.story("Неуспешная авторизация с невалидными данными")
    @allure.title("Логин с неверным паролем")
    @allure.tag("regression", "api", "login", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_invalid_password(self, api_manager: ApiManager, registered_user: UserRegisterResponse) -> None:
        """
        Тест на авторизацию пользователя c неверным паролем.
        """
        with allure.step("Подготовка данных с невалидным паролем"):
            login_data_with_invalid_password = {
                "email": registered_user.email,
                "password": "1000"
            }

        with allure.step("Попытка авторизации пользователя с невалидным паролем"):
            api_manager.auth_api.login_user(login_data_with_invalid_password, 401)

    @pytest.mark.regression
    @allure.story("Неуспешная авторизация с невалидными данными")
    @allure.title("Логин с пустым телом запроса")
    @allure.tag("regression", "api", "login", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_empty_body(self, api_manager: ApiManager) -> None:
        """
        Тест на авторизацию пользователя c пустым телом.
        """
        with allure.step("Попытка авторизации с пустым телом запроса"):
            api_manager.auth_api.login_user({}, 401)
