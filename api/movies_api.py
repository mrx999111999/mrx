from constants import BASE_URL_FOR_MOVIES_API, MOVIES_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    """
    Класс для работы с фильмами.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL_FOR_MOVIES_API)

    def get_movies(self, params=None, expected_status=200):
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

    def create_movie(self, movie_data, expected_status=201):
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
