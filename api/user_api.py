import requests
from typing import Any
from requests import Session
from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL_FOR_AUTH_API, USER_ENDPOINT
from models.models import UserRegisterRequest


class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url=BASE_URL_FOR_AUTH_API)

    def get_user(self, user_locator: str, expected_status: int = 200) -> requests.Response:
        """
        Получение информации о пользователе.
        :param user_locator: ID или Email пользователя
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"{USER_ENDPOINT}/{user_locator}",
            expected_status=expected_status
        )

    def create_user(self, user_data: dict[str, Any] | UserRegisterRequest,
                    expected_status: int = 201) -> requests.Response:
        """
        Создание пользователя.
        :param user_data: Данные для создания пользователя
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=USER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id: str, expected_status: int = 200) -> requests.Response:
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{USER_ENDPOINT}/{user_id}",
            expected_status=expected_status
        )

    def update_user(self, user_id: str, user_data: dict[str, Any], expected_status: int = 200) -> requests.Response:
        """
        Изменение данных пользователя.
        :param user_data: Данные, которые нужно изменить у пользователя
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="PATCH",
            endpoint=f"{USER_ENDPOINT}/{user_id}",
            data=user_data,
            expected_status=expected_status
        )
