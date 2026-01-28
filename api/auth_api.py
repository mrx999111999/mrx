import allure
import requests
from requests import Session
from constants import REGISTER_ENDPOINT
from constants import LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL_FOR_AUTH_API
from models.models import UserRegisterRequest, UserLoginRequest


class AuthAPI(CustomRequester):
    """
    Класс для работы с аутентификацией.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url=BASE_URL_FOR_AUTH_API)

    @allure.step("Регистрация нового пользователя")
    def register_user(self, user_data: UserRegisterRequest,
                      expected_status: int = 201) -> requests.Response:
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

    @allure.step("Авторизация пользователя")
    def login_user(self, login_data: UserLoginRequest,
                   expected_status: int = 200) -> requests.Response:
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

    def authenticate(self, user_creds: tuple[str, str]) -> None:
        """
        Авторизация пользователя и обновление хэдеров добавлением токена.
        :param user_creds: Данные для логина.
        """
        with allure.step("Распаковываем user_creds"):
            email, password = user_creds

        with allure.step("Отправка запроса на авторизацию"):
            login_data = UserLoginRequest(email=email, password=password)
            response = self.login_user(login_data).json()

        with allure.step("Проверяем наличие токена в ответе"):
            if "accessToken" not in response:
                raise KeyError("token is missing")

        with allure.step("Обновляем хэдеры, добавляя полученный токен"):
            self.update_session_headers(**{"authorization": f"Bearer {response['accessToken']}"})
