from constants import REGISTER_ENDPOINT
from constants import LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL_FOR_AUTH_API


class AuthAPI(CustomRequester):
    """
    Класс для работы с аутентификацией.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL_FOR_AUTH_API)

    def register_user(self, user_data, expected_status=201):
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status=200):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, login_data):
        """
        Авторизация пользователя и обновление хэдеров добавлением токена.
        :param login_data: Данные для логина.
        """
        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        self.update_session_headers(**{"authorization": f"Bearer {response['accessToken']}"})
