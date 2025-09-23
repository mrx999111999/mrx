import requests
from typing import Any
from requests import Session
from constants import BASE_URL_FOR_MOVIES_API, MOVIES_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    """
    Класс для работы с фильмами.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url=BASE_URL_FOR_MOVIES_API)

    def get_movies(self, params: dict[str, Any] | None = None, expected_status: int = 200) -> requests.Response:
        """
        Получение афиш фильмов.
        :param params: Словарь параметров
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            expected_status=expected_status,
            params=params
        )

    def create_movie(self, movie_data: dict[str, str | int | float | bool],
                     expected_status: int = 201) -> requests.Response:
        """
        Создание фильма.
        :param movie_data: Данные фильма
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id: int, expected_status: int = 200) -> requests.Response:
        """
        Удаление фильма.
        :param movie_id: Айди фильма
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )
