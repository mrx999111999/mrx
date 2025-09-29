import random
import pytest
from api.api_manager import ApiManager
from conftest import created_movie
from entities.user import User
from utils.data_generator import DataGeneratorForMoviesAPI


class TestMoviesApi:
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_movies(self, api_manager: ApiManager) -> None:
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

    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_movies_filtered_by_page_size(self, api_manager: ApiManager) -> None:
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

    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_movies_filtered_by_page(self, api_manager: ApiManager) -> None:
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

    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_movies_filtered_by_min_price(self, api_manager: ApiManager) -> None:
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

    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_movies_filtered_by_max_price(self, api_manager: ApiManager) -> None:
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

    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_movies_filtered_by_locations(self, api_manager: ApiManager) -> None:
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

    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_movies_filtered_by_genre_id(self, api_manager: ApiManager) -> None:
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

    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.parametrize("min_price,max_price,locations,genre_id", [(100, 2000, "MSK", 2), (1000, 3000, "SPB", 10)])
    def test_get_movies_with_multiple_filters(self, min_price: int | float, max_price: int | float, locations: str,
                                              genre_id: int,
                                              api_manager: ApiManager) -> None:
        """
        Параметризованный тест на получение афиш фильмов с комбинацией фильтров".
        """
        combined_filtered = {
            "minPrice": min_price,
            "maxPrice": max_price,
            "locations": locations,
            "genreId": genre_id,
        }
        response = api_manager.movies_api.get_movies(combined_filtered).json()

        # Проверки
        for movie in response["movies"]:
            assert min_price <= movie["price"] <= max_price, "price д.б >= minPrice и <= maxPrice"
            assert movie["location"] == locations, "locations не совпадает"
            assert movie["genreId"] == genre_id, "genreId не совпадает"

        assert "movies" in response, "movies отсутствует в ответе"
        assert response["movies"] != [], "Список фильмов пустой"
        assert "count" in response, "count отсутствует в ответе"
        assert "page" in response, "page отсутствует в ответе"
        assert "pageSize" in response, "pageSize отсутствует в ответе"
        assert "pageCount" in response, "pageCount отсутствует в ответе"

    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_movie(self, super_admin: User, test_movie: dict[str, str | int | float | bool], db_helper) -> None:
        """
        Тест на создание фильма с ролью "SUPER_ADMIN".
        """
        response = super_admin.api.movies_api.create_movie(test_movie).json()
        created_movie_in_db = db_helper.get_movie_by_id_from_db(response["id"]).to_dict()


        # Проверки
        assert "id" in response, "id отсутствует в ответе"
        assert "name" in response, "name отсутствует в ответе"
        assert test_movie["name"] == response["name"], "name не совпадает"
        assert "price" in response, "price отсутствует в ответе"
        assert test_movie["price"] == response["price"], "price не совпадает"
        assert "description" in response, "description отсутствует в ответе"
        assert test_movie["description"] == response["description"], "description не совпадает"
        assert "imageUrl" in response, "imageUrl отсутствует в ответе"
        assert test_movie["imageUrl"] == response["imageUrl"], "imageUrl не совпадает"
        assert "location" in response, "location отсутствует в ответе"
        assert test_movie["location"] == response["location"], "location не совпадает"
        assert "published" in response, "published отсутствует в ответе"
        assert test_movie["published"] == response["published"], "published не совпадает"
        assert "genreId" in response, "genreId отсутствует в ответе"
        assert test_movie["genreId"] == response["genreId"], "genreId не совпадает"
        assert "genre" in response, "genre отсутствует в ответе"
        assert "createdAt" in response, "createdAt отсутствует в ответе"
        assert "rating" in response, "rating отсутствует в ответе"

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.slow
    @pytest.mark.parametrize("count", [1, 2, 3], ids=[
        "delete_first_movie",
        "delete_second_movie",
        "delete_third_movie"
    ])
    def test_delete_movie(self, super_admin: User, created_movie: dict[
        str, str | int | float | bool], count: int) -> None:
        """
        Параметризованный тест на удаление фильма.
        """
        response = super_admin.api.movies_api.delete_movie(created_movie["id"]).json()

        # Проверки
        assert "id" in response, "id отсутствует в ответе"
        assert "name" in response, "name отсутствует в ответе"
        assert "price" in response, "price отсутствует в ответе"
        assert "description" in response, "description отсутствует в ответе"
        assert "imageUrl" in response, "imageUrl отсутствует в ответе"
        assert "location" in response, "location отсутствует в ответе"
        assert "published" in response, "published отсутствует в ответе"
        assert "genreId" in response, "genreId отсутствует в ответе"
        assert "genre" in response, "genre отсутствует в ответе"
        assert "createdAt" in response, "createdAt отсутствует в ответе"
        assert "rating" in response, "rating отсутствует в ответе"
        assert "reviews" in response, "reviews отсутствует в ответе"

    @pytest.mark.api
    @pytest.mark.regression
    def test_create_movie_without_name(self, super_admin: User,
                                       test_movie: dict[str, str | int | float | bool]) -> None:
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
        super_admin.api.movies_api.create_movie(movie_data_without_name, 400)

    @pytest.mark.api
    @pytest.mark.regression
    def test_create_movie_with_duplicate_name(self, super_admin: User, created_movie: dict[
        str, str | int | float | bool]) -> None:
        """
        Тест на создание фильма с уже существующим названием.
        """
        movie_data_with_duplicate_name = {
            "name": created_movie["name"],
            "imageUrl": created_movie["imageUrl"],
            "price": created_movie["price"],
            "description": created_movie["description"],
            "location": created_movie["location"],
            "published": created_movie["published"],
            "genreId": created_movie["genreId"],
        }
        super_admin.api.movies_api.create_movie(movie_data_with_duplicate_name, 409)

    @pytest.mark.api
    @pytest.mark.regression
    def test_create_movie_without_price(self, super_admin: User,
                                        test_movie: dict[str, str | int | float | bool]) -> None:
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
        super_admin.api.movies_api.create_movie(movie_data_without_price, 400)

    @pytest.mark.api
    @pytest.mark.regression
    def test_create_movie_without_description(self, super_admin: User,
                                              test_movie: dict[str, str | int | float | bool]) -> None:
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
        super_admin.api.movies_api.create_movie(movie_data_without_description, 400)

    @pytest.mark.api
    @pytest.mark.regression
    def test_create_movie_without_location(self, super_admin: User,
                                           test_movie: dict[str, str | int | float | bool]) -> None:
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
        super_admin.api.movies_api.create_movie(movie_data_without_location, 400)

    @pytest.mark.api
    @pytest.mark.regression
    def test_create_movie_without_published(self, super_admin: User,
                                            test_movie: dict[str, str | int | float | bool]) -> None:
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
        super_admin.api.movies_api.create_movie(movie_data_without_published, 400)

    @pytest.mark.api
    @pytest.mark.regression
    def test_create_movie_without_genre_id(self, super_admin: User,
                                           test_movie: dict[str, str | int | float | bool]) -> None:
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
        super_admin.api.movies_api.create_movie(movie_data_without_genre_id, 400)

    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.slow
    def test_create_movie_with_common_user(self, common: User, test_movie: dict[str, str | int | float | bool]) -> None:
        """
        Тест на создание фильма с ролью "USER".
        """
        common.api.movies_api.create_movie(test_movie, 403)

    @pytest.mark.api
    @pytest.mark.regression
    def test_get_movies_with_page_size_zero(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с "pageSize" равным 0.
        """
        filter_by_page_size = {"pageSize": 0}
        api_manager.movies_api.get_movies(filter_by_page_size, 400)

    @pytest.mark.api
    @pytest.mark.regression
    def test_get_movies_with_negative_page_size(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с отрицательным "pageSize".
        """
        filter_by_page_size = {"pageSize": -1}
        api_manager.movies_api.get_movies(filter_by_page_size, 400)

    @pytest.mark.api
    @pytest.mark.regression
    def test_get_movies_with_page_zero(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с "page" равным 0.
        """
        filter_by_page = {"page": 0}
        api_manager.movies_api.get_movies(filter_by_page, 400)

    @pytest.mark.api
    @pytest.mark.regression
    def test_get_movies_with_negative_page(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с отрицательным "page".
        """
        filter_by_page = {"page": -1}
        api_manager.movies_api.get_movies(filter_by_page, 400)
