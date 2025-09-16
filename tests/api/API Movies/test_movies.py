import random
from api.api_manager import ApiManager
from constants import CREDS_FOR_SUPER_ADMIN
from utils.data_generator import DataGeneratorForMoviesAPI


class TestMoviesApi:
    def test_get_movies(self, api_manager: ApiManager):
        """
        Тест на получение афиш фильмов с фильтрами по умолчанию.
        """
        response = api_manager.movies_api.get_movies()
        response_data = response.json()

        # Проверки
        assert "movies" in response_data, "movies отсутствует в ответе"
        assert response_data["movies"] != [], "Список фильмов пустой"
        assert "count" in response_data, "count отсутствует в ответе"
        assert "page" in response_data, "page отсутствует в ответе"
        assert "pageSize" in response_data, "pageSize отсутствует в ответе"
        assert "pageCount" in response_data, "pageCount отсутствует в ответе"

    def test_get_movies_filtered_by_page_size(self, api_manager: ApiManager):
        """
        Тест на получение афиш фильмов с явным указанием фильтра "pageSize".
        """
        filter_by_page_size = {"pageSize": random.randint(1, 10)}
        response = api_manager.movies_api.get_movies(filter_by_page_size)
        response_data = response.json()

        # Проверки
        assert "movies" in response_data, "movies отсутствует в ответе"
        assert response_data["movies"] != [], "Список фильмов пустой"
        assert "count" in response_data, "count отсутствует в ответе"
        assert "page" in response_data, "page отсутствует в ответе"
        assert "pageSize" in response_data, "pageSize отсутствует в ответе"
        assert response_data["pageSize"] == filter_by_page_size["pageSize"], "pageSize не совпадает с переданным"
        assert len(response_data["movies"]) == filter_by_page_size[
            "pageSize"], "Количество отображенных фильмов на странице не равно переданному в pageSize"
        assert "pageCount" in response_data, "pageCount отсутствует в ответе"

    def test_get_movies_filtered_by_page(self, api_manager: ApiManager):
        """
        Тест на получение афиш фильмов с явным указанием фильтра "page".
        """
        filter_by_page = {"page": random.randint(1, 10)}
        response = api_manager.movies_api.get_movies(filter_by_page)
        response_data = response.json()

        # Проверки
        assert "movies" in response_data, "movies отсутствует в ответе"
        assert response_data["movies"] != [], "Список фильмов пустой"
        assert "count" in response_data, "count отсутствует в ответе"
        assert "page" in response_data, "page отсутствует в ответе"
        assert response_data["page"] == filter_by_page["page"], "page не совпадает с переданным"
        assert "pageSize" in response_data, "pageSize отсутствует в ответе"
        assert "pageCount" in response_data, "pageCount отсутствует в ответе"

    def test_get_movies_filtered_by_min_price(self, api_manager: ApiManager):
        """
        Тест на получение афиш фильмов с явным указанием фильтра "minPrice".
        """
        filter_by_min_price = {"minPrice": random.randint(1, 500)}
        response = api_manager.movies_api.get_movies(filter_by_min_price)
        response_data = response.json()

        # Проверки
        for movie in response_data["movies"]:
            assert movie["price"] > filter_by_min_price["minPrice"], "price меньше, чем minPrice"
        assert "movies" in response_data, "movies отсутствует в ответе"
        assert response_data["movies"] != [], "Список фильмов пустой"
        assert "count" in response_data, "count отсутствует в ответе"
        assert "page" in response_data, "page отсутствует в ответе"
        assert "pageSize" in response_data, "pageSize отсутствует в ответе"
        assert "pageCount" in response_data, "pageCount отсутствует в ответе"

    def test_get_movies_filtered_by_max_price(self, api_manager: ApiManager):
        """
        Тест на получение афиш фильмов с явным указанием фильтра "maxPrice".
        """
        filter_by_max_price = {"maxPrice": random.randint(1500, 5000)}
        response = api_manager.movies_api.get_movies(filter_by_max_price)
        response_data = response.json()

        # Проверки
        for movie in response_data["movies"]:
            assert movie["price"] < filter_by_max_price["maxPrice"], "price больше, чем maxPrice"
        assert "movies" in response_data, "movies отсутствует в ответе"
        assert response_data["movies"] != [], "Список фильмов пустой"
        assert "count" in response_data, "count отсутствует в ответе"
        assert "page" in response_data, "page отсутствует в ответе"
        assert "pageSize" in response_data, "pageSize отсутствует в ответе"
        assert "pageCount" in response_data, "pageCount отсутствует в ответе"

    def test_get_movies_filtered_by_locations(self, api_manager: ApiManager):
        """
        Тест на получение афиш фильмов с явным указанием фильтра "locations".
        """
        locations = [DataGeneratorForMoviesAPI.generate_random_location()]
        filter_by_locations = {"locations": locations}
        response = api_manager.movies_api.get_movies(filter_by_locations)
        response_data = response.json()

        # Проверки
        for movie in response_data["movies"]:
            assert movie["location"] == locations[0], "location не совпадает"
        assert "movies" in response_data, "movies отсутствует в ответе"
        assert response_data["movies"] != [], "Список фильмов пустой"
        assert "count" in response_data, "count отсутствует в ответе"
        assert "page" in response_data, "page отсутствует в ответе"
        assert "pageSize" in response_data, "pageSize отсутствует в ответе"
        assert "pageCount" in response_data, "pageCount отсутствует в ответе"

    def test_get_movies_filtered_by_genre_id(self, api_manager: ApiManager):
        """
        Тест на получение афиш фильмов с явным указанием фильтра "genreId".
        """
        genre_id = DataGeneratorForMoviesAPI.generate_random_genre_id()
        filter_by_genre_id = {"genreId": genre_id}
        response = api_manager.movies_api.get_movies(filter_by_genre_id)
        response_data = response.json()

        # Проверки
        for movie in response_data["movies"]:
            assert movie["genreId"] == genre_id, "genreId не совпадает"
        assert "movies" in response_data, "movies отсутствует в ответе"
        assert response_data["movies"] != [], "Список фильмов пустой"
        assert "count" in response_data, "count отсутствует в ответе"
        assert "page" in response_data, "page отсутствует в ответе"
        assert "pageSize" in response_data, "pageSize отсутствует в ответе"
        assert "pageCount" in response_data, "pageCount отсутствует в ответе"

    def test_create_movie(self, api_manager: ApiManager, test_movie):
        """
        Тест на создание фильма.
        """
        # Авторизуемся под ролью SUPER_ADMIN и обновляем хэдеры
        api_manager.auth_api.authenticate(CREDS_FOR_SUPER_ADMIN)

        response = api_manager.movies_api.create_movie(test_movie)
        response_data = response.json()

        # Проверки
        assert "id" in response_data, "id отсутствует в ответе"
        assert "name" in response_data, "name отсутствует в ответе"
        assert test_movie["name"] == response_data["name"], "name не совпадает"
        assert "price" in response_data, "price отсутствует в ответе"
        assert test_movie["price"] == response_data["price"], "price не совпадает"
        assert "description" in response_data, "description отсутствует в ответе"
        assert test_movie["description"] == response_data["description"], "description не совпадает"
        assert "imageUrl" in response_data, "imageUrl отсутствует в ответе"
        assert test_movie["imageUrl"] == response_data["imageUrl"], "imageUrl не совпадает"
        assert "location" in response_data, "location отсутствует в ответе"
        assert test_movie["location"] == response_data["location"], "location не совпадает"
        assert "published" in response_data, "published отсутствует в ответе"
        assert test_movie["published"] == response_data["published"], "published не совпадает"
        assert "genreId" in response_data, "genreId отсутствует в ответе"
        assert test_movie["genreId"] == response_data["genreId"], "genreId не совпадает"
        assert "genre" in response_data, "genre отсутствует в ответе"
        assert "createdAt" in response_data, "createdAt отсутствует в ответе"
        assert "rating" in response_data, "rating отсутствует в ответе"

    def test_create_movie_without_name(self, api_manager: ApiManager, test_movie):
        """
        Тест на создание фильма без "name" в запросе.
        """
        movie_data_without_name = {
            "imageUrl": test_movie["imageUrl"],
            "price": test_movie["price"],
            "description": test_movie["description"],
            "location": test_movie["location"],
            "published": test_movie["published"],
            "genreId": test_movie["genreId"],
        }
        response = api_manager.movies_api.create_movie(movie_data_without_name, 400)

        # Проверки
        assert response.text is not None, "Пустое тело ответа"

    def test_create_movie_with_duplicate_name(self, api_manager: ApiManager, test_movie):
        """
        Тест на создание фильма с уже существующим названием.
        """
        movie_data_with_duplicate_name = {
            "name": test_movie["name"],
            "imageUrl": test_movie["imageUrl"],
            "price": test_movie["price"],
            "description": test_movie["description"],
            "location": test_movie["location"],
            "published": test_movie["published"],
            "genreId": test_movie["genreId"],
        }
        response = api_manager.movies_api.create_movie(movie_data_with_duplicate_name, 409)

        # Проверки
        assert response.text is not None, "Пустое тело ответа"

    def test_create_movie_without_price(self, api_manager: ApiManager, test_movie):
        """
        Тест на создание фильма без "price" в запросе.
        """
        movie_data_without_price = {
            "name": "some_movie",
            "imageUrl": test_movie["imageUrl"],
            "description": test_movie["description"],
            "location": test_movie["location"],
            "published": test_movie["published"],
            "genreId": test_movie["genreId"],
        }
        response = api_manager.movies_api.create_movie(movie_data_without_price, 400)

        # Проверки
        assert response.text is not None, "Пустое тело ответа"

    def test_create_movie_without_description(self, api_manager: ApiManager, test_movie):
        """
        Тест на создание фильма без "description" в запросе.
        """
        movie_data_without_description = {
            "name": "some_movie",
            "imageUrl": test_movie["imageUrl"],
            "price": test_movie["price"],
            "location": test_movie["location"],
            "published": test_movie["published"],
            "genreId": test_movie["genreId"],
        }
        response = api_manager.movies_api.create_movie(movie_data_without_description, 400)

        # Проверки
        assert response.text is not None, "Пустое тело ответа"

    def test_create_movie_without_location(self, api_manager: ApiManager, test_movie):
        """
        Тест на создание фильма без "location" в запросе.
        """
        movie_data_without_location = {
            "name": "some_movie",
            "imageUrl": test_movie["imageUrl"],
            "price": test_movie["price"],
            "description": test_movie["description"],
            "published": test_movie["published"],
            "genreId": test_movie["genreId"],
        }
        response = api_manager.movies_api.create_movie(movie_data_without_location, 400)

        # Проверки
        assert response.text is not None, "Пустое тело ответа"

    def test_create_movie_without_published(self, api_manager: ApiManager, test_movie):
        """
        Тест на создание фильма без "published" в запросе.
        """
        movie_data_without_published = {
            "name": "some_movie",
            "imageUrl": test_movie["imageUrl"],
            "price": test_movie["price"],
            "description": test_movie["description"],
            "location": test_movie["location"],
            "genreId": test_movie["genreId"],
        }
        response = api_manager.movies_api.create_movie(movie_data_without_published, 400)

        # Проверки
        assert response.text is not None, "Пустое тело ответа"

    def test_create_movie_without_genre_id(self, api_manager: ApiManager, test_movie):
        """
        Тест на создание фильма без "genreId" в запросе.
        """
        movie_data_without_genre_id = {
            "name": "some_movie",
            "imageUrl": test_movie["imageUrl"],
            "price": test_movie["price"],
            "description": test_movie["description"],
            "location": test_movie["location"],
            "published": test_movie["published"]
        }
        response = api_manager.movies_api.create_movie(movie_data_without_genre_id, 400)

        # Проверки
        assert response.text is not None, "Пустое тело ответа"

    def test_get_movies_with_page_size_zero(self, api_manager: ApiManager):
        """
        Тест на получение афиш фильмов с "pageSize" равным 0.
        """
        filter_by_page_size = {"pageSize": 0}
        response = api_manager.movies_api.get_movies(filter_by_page_size, 400)

        # Проверки
        assert response.text is not None, "Пустое тело ответа"

    def test_get_movies_with_negative_page_size(self, api_manager: ApiManager):
        """
        Тест на получение афиш фильмов с отрицательным "pageSize".
        """
        filter_by_page_size = {"pageSize": -1}
        response = api_manager.movies_api.get_movies(filter_by_page_size, 400)

        # Проверки
        assert response.text is not None, "Пустое тело ответа"

    def test_get_movies_with_page_zero(self, api_manager: ApiManager):
        """
        Тест на получение афиш фильмов с "page" равным 0.
        """
        filter_by_page = {"page": 0}
        response = api_manager.movies_api.get_movies(filter_by_page, 400)

        # Проверки
        assert response.text is not None, "Пустое тело ответа"

    def test_get_movies_with_negative_page(self, api_manager: ApiManager):
        """
        Тест на получение афиш фильмов с отрицательным "page".
        """
        filter_by_page = {"page": -1}
        response = api_manager.movies_api.get_movies(filter_by_page, 400)

        # Проверки
        assert response.text is not None, "Пустое тело ответа"
