import allure
import requests
from requests import Session
from constants import BASE_URL_FOR_MOVIES_API, MOVIES_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from models.models import CreateMovieRequest, ParamsForGetMoviesRequest


class MoviesAPI(CustomRequester):
    """
    Класс для работы с фильмами.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url=BASE_URL_FOR_MOVIES_API)

    @allure.step("Получение списка фильмов")
    def get_movies(self, params: ParamsForGetMoviesRequest = None, expected_status: int = 200) -> requests.Response:
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

    @allure.step("Создание нового фильма")
    def create_movie(self, movie_data: CreateMovieRequest,
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

    @allure.step("Удаление фильма")
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
