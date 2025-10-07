import allure
import pytest
from pytest_check import check

from db_requester.db_helpers import DBHelper
from entities.user import User
from enums.roles import Roles
from models.models import UserRegisterRequest, UserRegisterResponse


@pytest.mark.api
@allure.epic("Auth API")
@allure.feature("Пользователь")
class TestUser:
    @pytest.mark.smoke
    @allure.story("Успешное создание нового пользователя")
    @allure.title("Создание пользователя через роль SUPER_ADMIN")
    @allure.tag("smoke", "api", "creation")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_user_with_super_admin(self, super_admin: User, creation_user_data: UserRegisterRequest,
                                          db_helper: DBHelper) -> None:
        """
        Тест на создание пользователя с использованием роли "SUPER_ADMIN".
        """
        with allure.step("Создание пользователя через API"):
            response = super_admin.api.user_api.create_user(creation_user_data).json()
            response_data = UserRegisterResponse(
                **response)  # Используем модель ответа для регистрации пользователя, т.к. структуры ответа у них совпадают

        with allure.step("Получение данных пользователя из БД"):
            db_user = db_helper.get_user_by_id(response_data.id)

        with allure.step("Проверки API ответа"):
            with check:
                assert response_data.email == creation_user_data.email, "email не совпадает"
                assert response_data.fullName == creation_user_data.fullName, "fullName не совпадает"
                assert response_data.roles == creation_user_data.roles, "roles не совпадает"
                assert response_data.verified is True, "verified должен быть True"
                assert response_data.banned is False, "banned должен быть False"

        with allure.step("Проверки в БД"):
            with check:
                assert db_user is not None, "Пользователь не найден в БД"
                assert db_user.id == response_data.id, "id в БД не совпадает"
                assert db_user.email == creation_user_data.email, "email в БД не совпадает"
                assert db_user.full_name == creation_user_data.fullName, "fullName в БД не совпадает"
                assert db_user.password != creation_user_data.password, "Пароль должен быть захэширован"
                assert db_user.verified == True, "Пользователь должен быть верифицирован"
                assert db_user.banned == False, "Пользователь не должен быть забанен"
                assert Roles.USER.value in db_user.roles, "Роль USER должна быть в БД"
                assert db_user.created_at is not None, "Дата создания должна быть заполнена"
                assert db_user.updated_at is not None, "Дата обновления должна быть заполнена"

    @pytest.mark.smoke
    @allure.story("Получение данных пользователя")
    @allure.title("Получение пользователя по локатору (id/email) через роль SUPER_ADMIN")
    @allure.tag("smoke", "api")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_user_by_locator(self, super_admin: User, creation_user_data: UserRegisterRequest) -> None:
        """
        Тест на получение пользователя по локатору с использованием роли "SUPER_ADMIN".
        """
        with allure.step("Создание тестового пользователя и получение данных по нему"):
            response_created_user = super_admin.api.user_api.create_user(creation_user_data).json()
            response_get_user_by_id = super_admin.api.user_api.get_user(response_created_user['id']).json()
            user_by_id = UserRegisterResponse(**response_get_user_by_id)
            response_get_user_by_email = super_admin.api.user_api.get_user(creation_user_data.email).json()

        with allure.step("Проверки API ответа"):
            with check:
                assert response_get_user_by_id == response_get_user_by_email, "Содержание ответов должно быть идентичным"
                assert user_by_id.email == creation_user_data.email, "email не совпадает"
                assert user_by_id.fullName == creation_user_data.fullName, "fullName не совпадает"
                assert user_by_id.roles == creation_user_data.roles, "roles не совпадает"
                assert user_by_id.verified is True, "verified должен быть True"
                assert user_by_id.banned is False, "banned должен быть False"

    @pytest.mark.smoke
    @pytest.mark.slow
    @allure.story("Успешное создание нового пользователя")
    @allure.title("Создание пользователя через роль ADMIN")
    @allure.tag("smoke", "api", "creation")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_user_with_admin(self, admin: User, creation_user_data: UserRegisterRequest,
                                    db_helper: DBHelper) -> None:
        """
        Тест на создание пользователя с использованием роли "ADMIN".
        """
        with allure.step("Создание пользователя через API"):
            response = admin.api.user_api.create_user(creation_user_data).json()
            response_data = UserRegisterResponse(
                **response)  # Используем модель ответа для регистрации пользователя, т.к. структуры ответа у них совпадают

        with allure.step("Получение данных пользователя из БД"):
            db_user = db_helper.get_user_by_id(response_data.id)

        with allure.step("Проверки API ответа"):
            with check:
                assert response_data.email == creation_user_data.email, "email не совпадает"
                assert response_data.fullName == creation_user_data.fullName, "fullName не совпадает"
                assert response_data.roles == creation_user_data.roles, "roles не совпадает"
                assert response_data.verified is True, "verified должен быть True"
                assert response_data.banned is False, "banned должен быть False"

        with allure.step("Проверки в БД"):
            with check:
                assert db_user is not None, "Пользователь не найден в БД"
                assert db_user.id == response_data.id, "id в БД не совпадает"
                assert db_user.email == creation_user_data.email, "email в БД не совпадает"
                assert db_user.full_name == creation_user_data.fullName, "fullName в БД не совпадает"
                assert db_user.password != creation_user_data.password, "Пароль должен быть захэширован"
                assert db_user.verified == True, "Пользователь должен быть верифицирован"
                assert db_user.banned == False, "Пользователь не должен быть забанен"
                assert Roles.USER.value in db_user.roles, "Роль USER должна быть в БД"
                assert db_user.created_at is not None, "Дата создания должна быть заполнена"
                assert db_user.updated_at is not None, "Дата обновления должна быть заполнена"

    @pytest.mark.regression
    @pytest.mark.slow
    @allure.story("Неуспешное получение данных пользователя")
    @allure.title("Получение пользователя по локатору (id/email) через роль USER")
    @allure.tag("regression", "api", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_by_email_with_common_user(self, common: User) -> None:
        """
        Тест проверяет, что пользователь с ролью USER не может получить данные пользователя по email.
        """
        with allure.step("Попытка получения данных пользователя через роль USER"):
            common.api.user_api.get_user(common.email, expected_status=403)
