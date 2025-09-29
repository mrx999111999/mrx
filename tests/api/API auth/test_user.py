import pytest
from entities.user import User
from models.test_user import UserRegisterRequest, UserRegisterResponse


class TestUser:
    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_user_with_super_admin(self, super_admin: User, creation_user_data: UserRegisterRequest) -> None:
        """
        Тест на создание пользователя с использованием роли "SUPER_ADMIN".
        """
        response = super_admin.api.user_api.create_user(creation_user_data)
        response_data = UserRegisterResponse(**response.json())

        # Проверки
        assert response_data.email == creation_user_data.email
        assert response_data.fullName == creation_user_data.fullName
        assert response_data.roles == creation_user_data.roles
        assert response_data.verified is True

    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_user_by_locator(self, super_admin: User, creation_user_data: UserRegisterRequest) -> None:
        """
        Тест на получение пользователя по локатору.
        """
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        user_by_id = UserRegisterResponse(**response_by_id)
        response_by_email = super_admin.api.user_api.get_user(creation_user_data.email).json()

        # Проверки
        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert user_by_id.email == creation_user_data.email
        assert user_by_id.fullName == creation_user_data.fullName
        assert user_by_id.roles == creation_user_data.roles
        assert user_by_id.verified is True

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.slow
    def test_create_user_with_admin(self, admin: User, creation_user_data: UserRegisterRequest) -> None:
        """
        Тест на создание пользователя с использованием роли "ADMIN".
        """
        response = admin.api.user_api.create_user(creation_user_data)
        response_data = UserRegisterResponse(**response.json())

        # Проверки
        assert response_data.email == creation_user_data.email
        assert response_data.fullName == creation_user_data.fullName
        assert response_data.roles == creation_user_data.roles
        assert response_data.verified is True

    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.slow
    def test_get_user_by_email_with_common_user(self, common: User) -> None:
        common.api.user_api.get_user(common.email, expected_status=403)
