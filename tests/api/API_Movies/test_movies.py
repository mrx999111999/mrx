import random
import allure
import pytest
from pytest_check import check
from api.api_manager import ApiManager
from conftest import created_movie
from db_requester.db_helpers import DBHelper
from entities.user import User
from models.models import GetMoviesResponse, CreateMovieRequest, CreateMovieResponse, DeleteMovieResponse
from utils.data_generator import DataGeneratorForMoviesAPI


@pytest.mark.api
@allure.epic("Movies API")
@allure.feature("Фильмы")
class TestMoviesApi:
    @pytest.mark.smoke
    @allure.story("Получение афиш фильмов")
    @allure.title("Успешное получение афиш фильмов с фильтрами по умолчанию")
    @allure.tag("smoke", "api")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_movies(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с фильтрами по умолчанию.
        """
        with allure.step("Получение афиш фильмов"):
            response = api_manager.movies_api.get_movies().json()
            response_data = GetMoviesResponse(**response)

        with allure.step(
                "Подготовка обязательных полей для проверки списка movies с ответа"):
            required_fields = {
                "id", "name", "price", "description", "imageUrl",
                "location", "published", "genreId", "genre", "createdAt", "rating"
            }

        with allure.step("Проверки API ответа"):
            with check:
                assert len(
                    response_data.movies) == response_data.pageSize, "Количество отображенных фильмов на странице не равно переданному в pageSize"
                for movie in response_data.movies:
                    assert required_fields.issubset(
                        movie.keys()), f"Отсутствуют поля в movie: {required_fields - movie.keys()}"

    @pytest.mark.smoke
    @allure.story("Получение афиш фильмов")
    @allure.title("Успешное получение афиш фильмов с фильтром pageSize")
    @allure.tag("smoke", "api")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_movies_filtered_by_page_size(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с явным указанием фильтра "pageSize".
        """
        with allure.step("Получение афиш фильмов"):
            filter_by_page_size = {"pageSize": random.randint(1, 10)}
            response = api_manager.movies_api.get_movies(filter_by_page_size).json()
            response_data = GetMoviesResponse(**response)

        with allure.step("Проверки API ответа"):
            with check:
                assert response_data.pageSize == filter_by_page_size["pageSize"], "pageSize не совпадает с переданным"
                assert len(response_data.movies) == filter_by_page_size[
                    "pageSize"], "Количество отображенных фильмов на странице не равно переданному в pageSize"

    @pytest.mark.smoke
    @allure.story("Получение афиш фильмов")
    @allure.title("Успешное получение афиш фильмов с фильтром page")
    @allure.tag("smoke", "api")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_movies_filtered_by_page(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с явным указанием фильтра "page".
        """
        with allure.step("Получение афиш фильмов"):
            filter_by_page = {"page": random.randint(1, 10)}
            response = api_manager.movies_api.get_movies(filter_by_page).json()
            response_data = GetMoviesResponse(**response)

        with allure.step("Проверки API ответа"):
            assert response_data.page == filter_by_page["page"], "page не совпадает с переданным"

    @pytest.mark.smoke
    @allure.story("Получение афиш фильмов")
    @allure.title("Успешное получение афиш фильмов с фильтром minPrice")
    @allure.tag("smoke", "api")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_movies_filtered_by_min_price(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с явным указанием фильтра "minPrice".
        """
        with allure.step("Получение афиш фильмов"):
            filter_by_min_price = {"minPrice": random.randint(1, 500)}
            response = api_manager.movies_api.get_movies(filter_by_min_price).json()
            response_data = GetMoviesResponse(**response)

        with allure.step("Проверки API ответа"):
            with check:
                for movie in response_data.movies:
                    assert movie["price"] > filter_by_min_price["minPrice"], "price меньше, чем minPrice"

    @pytest.mark.smoke
    @allure.story("Получение афиш фильмов")
    @allure.title("Успешное получение афиш фильмов с фильтром maxPrice")
    @allure.tag("smoke", "api")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_movies_filtered_by_max_price(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с явным указанием фильтра "maxPrice".
        """
        with allure.step("Получение афиш фильмов"):
            filter_by_max_price = {"maxPrice": random.randint(1500, 5000)}
            response = api_manager.movies_api.get_movies(filter_by_max_price).json()
            response_data = GetMoviesResponse(**response)

        with allure.step("Проверки API ответа"):
            with check:
                for movie in response_data.movies:
                    assert movie["price"] < filter_by_max_price["maxPrice"], "price больше, чем maxPrice"

    @pytest.mark.smoke
    @allure.story("Получение афиш фильмов")
    @allure.title("Успешное получение афиш фильмов с фильтром locations")
    @allure.tag("smoke", "api")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_movies_filtered_by_locations(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с явным указанием фильтра "locations".
        """
        with allure.step("Получение афиш фильмов"):
            locations = [DataGeneratorForMoviesAPI.generate_random_location()]
            filter_by_locations = {"locations": locations}
            response = api_manager.movies_api.get_movies(filter_by_locations).json()
            response_data = GetMoviesResponse(**response)

        with allure.step("Проверки API ответа"):
            with check:
                for movie in response_data.movies:
                    assert movie["location"] in locations, "location не совпадает"

    @pytest.mark.smoke
    @allure.story("Получение афиш фильмов")
    @allure.title("Успешное получение афиш фильмов с фильтром genreId")
    @allure.tag("smoke", "api")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_movies_filtered_by_genre_id(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с явным указанием фильтра "genreId".
        """
        with allure.step("Получение афиш фильмов"):
            genre_id = DataGeneratorForMoviesAPI.generate_random_genre_id()
            filter_by_genre_id = {"genreId": genre_id}
            response = api_manager.movies_api.get_movies(filter_by_genre_id).json()
            response_data = GetMoviesResponse(**response)

        with allure.step("Проверки API ответа"):
            with check:
                for movie in response_data.movies:
                    assert movie["genreId"] == genre_id, "genreId не совпадает"

    @pytest.mark.regression
    @pytest.mark.parametrize("min_price,max_price,locations,genre_id", [(100, 2000, "MSK", 2), (1000, 3000, "SPB", 10)])
    @allure.story("Получение афиш фильмов")
    @allure.title("Успешное получение афиш фильмов с комбинированными фильтрами")
    @allure.tag("regression", "api")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_with_multiple_filters(self, min_price: int | float, max_price: int | float, locations: str,
                                              genre_id: int,
                                              api_manager: ApiManager) -> None:
        """
        Параметризованный тест на получение афиш фильмов с комбинацией фильтров".
        """
        with allure.step("Подготовка фильтров"):
            combined_filtered = {
                "minPrice": min_price,
                "maxPrice": max_price,
                "locations": locations,
                "genreId": genre_id,
            }

        with allure.step("Получение афиш фильмов"):
            response = api_manager.movies_api.get_movies(combined_filtered).json()
            response_data = GetMoviesResponse(**response)

        with allure.step("Проверки API ответа"):
            with check:
                for movie in response_data.movies:
                    assert min_price <= movie["price"] <= max_price, "price д.б >= minPrice и <= maxPrice"
                    assert movie["location"] == locations, "location не совпадает"
                    assert movie["genreId"] == genre_id, "genreId не совпадает"

    @pytest.mark.smoke
    @allure.story("Создание фильма")
    @allure.title("Успешное создание фильма с использованием роли SUPER_ADMIN")
    @allure.tag("smoke", "api")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_movie(self, super_admin: User, test_movie: CreateMovieRequest, db_helper: DBHelper) -> None:
        """
        Тест на создание фильма с ролью "SUPER_ADMIN".
        """
        with allure.step("Создание фильма"):
            response = super_admin.api.movies_api.create_movie(test_movie).json()
            response_data = CreateMovieResponse(**response)

        with allure.step("Получение данных фильма из БД"):
            db_movie = db_helper.get_movie_by_id_from_db(response_data.id)

        with allure.step("Проверки API ответа"):
            with check:
                assert test_movie.name == response_data.name, "name не совпадает"
                assert test_movie.price == response_data.price, "price не совпадает"
                assert test_movie.description == response_data.description, "description не совпадает"
                assert test_movie.imageUrl == response_data.imageUrl, "imageUrl не совпадает"
                assert test_movie.location == response_data.location, "location не совпадает"
                assert test_movie.published == response_data.published, "published не совпадает"
                assert test_movie.genreId == response_data.genreId, "genreId не совпадает"

        with allure.step("Проверки в БД"):
            with check:
                assert db_movie is not None, "Фильм не найден в БД"
                assert db_movie.id == response_data.id, "id в БД не совпадает"
                assert db_movie.name == response_data.name, "name в БД не совпадает"
                assert db_movie.price == response_data.price, "price в БД не совпадает"
                assert db_movie.description == response_data.description, "description в БД не совпадает"
                assert db_movie.image_url == response_data.imageUrl, "image_url в БД не совпадает"
                assert db_movie.location == response_data.location, "location в БД не совпадает"
                assert db_movie.published == response_data.published, "published в БД не совпадает"
                assert db_movie.genre_id == response_data.genreId, "genre_id в БД не совпадает"
                assert db_movie.rating == 0, "rating по умолчанию должен быть 0"
                assert db_movie.created_at is not None, "created_at должен быть заполнен"

    @pytest.mark.smoke
    @pytest.mark.slow
    @pytest.mark.parametrize("count", [1, 2, 3], ids=[
        "delete_first_movie",
        "delete_second_movie",
        "delete_third_movie"
    ])
    @allure.story("Удаление фильма")
    @allure.title("Успешное удаление фильма с использованием роли SUPER_ADMIN")
    @allure.tag("smoke", "api")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_delete_movie(self, super_admin: User, created_movie: CreateMovieResponse, count: int,
                          db_helper: DBHelper) -> None:
        """
        Параметризованный тест на удаление фильма с ролью "SUPER_ADMIN".
        """
        with allure.step("Удаление фильма"):
            response = super_admin.api.movies_api.delete_movie(created_movie.id).json()
            response_data = DeleteMovieResponse(**response)

        with allure.step("Получение данных фильма из БД"):
            db_movie = db_helper.get_movie_by_id_from_db(response_data.id)

        with allure.step("Проверки API ответа"):
            with check:
                assert response_data.id == created_movie.id, "id не совпадает"
                assert response_data.name == created_movie.name, "name не совпадает"
                assert response_data.price == created_movie.price, "price не совпадает"
                assert response_data.description == created_movie.description, "description не совпадает"
                assert response_data.imageUrl == created_movie.imageUrl, "imageUrl не совпадает"
                assert response_data.location == created_movie.location, "location не совпадает"
                assert response_data.published == created_movie.published, "published не совпадает"
                assert response_data.genreId == created_movie.genreId, "genreId не совпадает"

        with allure.step("Проверки в БД"):
            assert db_movie is None, "Фильм должен быть удален из базы"

    @pytest.mark.regression
    @allure.story("Неуспешное создание фильма")
    @allure.title("Попытка создания фильма без name в запросе")
    @allure.tag("regression", "api", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_without_name(self, super_admin: User,
                                       test_movie: CreateMovieRequest) -> None:
        """
        Тест на создание фильма без "name" в запросе.
        """
        with allure.step("Попытка создания фильма без name в запросе"):
            movie_data_without_name = test_movie.model_dump()
            del movie_data_without_name["name"]

            super_admin.api.movies_api.create_movie(movie_data_without_name, 400)

    @pytest.mark.regression
    @allure.story("Неуспешное создание фильма")
    @allure.title("Попытка создания фильма с уже существующим названием")
    @allure.tag("regression", "api", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_with_duplicate_name(self, super_admin: User, created_movie: CreateMovieResponse) -> None:
        """
        Тест на создание фильма с уже существующим названием.
        """
        with allure.step("Подготовка данных с дублирующим названием"):
            movie_data_with_duplicate_name = {
                "name": created_movie.name,
                "imageUrl": created_movie.imageUrl,
                "price": created_movie.price,
                "description": created_movie.description,
                "location": created_movie.location,
                "published": created_movie.published,
                "genreId": created_movie.genreId,
            }

        with allure.step("Попытка создания фильма с уже существующим названием"):
            super_admin.api.movies_api.create_movie(movie_data_with_duplicate_name, 409)

    @pytest.mark.regression
    @allure.story("Неуспешное создание фильма")
    @allure.title("Попытка создания фильма без price в запросе")
    @allure.tag("regression", "api", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_without_price(self, super_admin: User,
                                        test_movie: CreateMovieRequest) -> None:
        """
        Тест на создание фильма без "price" в запросе.
        """
        with allure.step("Попытка создания фильма без price в запросе"):
            movie_data_without_price = test_movie.model_dump()
            del movie_data_without_price["price"]

            super_admin.api.movies_api.create_movie(movie_data_without_price, 400)

    @pytest.mark.regression
    @allure.story("Неуспешное создание фильма")
    @allure.title("Попытка создания фильма без description в запросе")
    @allure.tag("regression", "api", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_without_description(self, super_admin: User,
                                              test_movie: CreateMovieRequest) -> None:
        """
        Тест на создание фильма без "description" в запросе.
        """
        with allure.step("Попытка создания фильма без description в запросе"):
            movie_data_without_description = test_movie.model_dump()
            del movie_data_without_description["description"]

            super_admin.api.movies_api.create_movie(movie_data_without_description, 400)

    @pytest.mark.regression
    @allure.story("Неуспешное создание фильма")
    @allure.title("Попытка создания фильма без location в запросе")
    @allure.tag("regression", "api", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_without_location(self, super_admin: User,
                                           test_movie: CreateMovieRequest) -> None:
        """
        Тест на создание фильма без "location" в запросе.
        """
        with allure.step("Попытка создания фильма без location в запросе"):
            movie_data_without_location = test_movie.model_dump()
            del movie_data_without_location["location"]

            super_admin.api.movies_api.create_movie(movie_data_without_location, 400)

    @pytest.mark.regression
    @allure.story("Неуспешное создание фильма")
    @allure.title("Попытка создания фильма без published в запросе")
    @allure.tag("regression", "api", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_without_published(self, super_admin: User,
                                            test_movie: CreateMovieRequest) -> None:
        """
        Тест на создание фильма без "published" в запросе.
        """
        with allure.step("Попытка создания фильма без published в запросе"):
            movie_data_without_published = test_movie.model_dump()
            del movie_data_without_published["published"]

            super_admin.api.movies_api.create_movie(movie_data_without_published, 400)

    @pytest.mark.regression
    @allure.story("Неуспешное создание фильма")
    @allure.title("Попытка создания фильма без genreId в запросе")
    @allure.tag("regression", "api", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_without_genre_id(self, super_admin: User,
                                           test_movie: CreateMovieRequest) -> None:
        """
        Тест на создание фильма без "genreId" в запросе.
        """
        with allure.step("Попытка создания фильма без genreId в запросе"):
            movie_data_without_genre_id = test_movie.model_dump()
            del movie_data_without_genre_id["genreId"]

            super_admin.api.movies_api.create_movie(movie_data_without_genre_id, 400)

    @pytest.mark.regression
    @pytest.mark.slow
    @allure.story("Неуспешное создание фильма")
    @allure.title("Попытка создания фильма с использованием роли USER")
    @allure.tag("regression", "api", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_with_common_user(self, common: User, test_movie: CreateMovieRequest) -> None:
        """
        Тест на создание фильма с ролью "USER".
        """
        with allure.step("Попытка создания фильма с использованием роли USER"):
            common.api.movies_api.create_movie(test_movie, 403)

    @pytest.mark.regression
    @pytest.mark.slow
    @allure.story("Неуспешное получение афиш фильмов")
    @allure.title("Попытка получения афиш фильмов с pageSize равным 0")
    @allure.tag("regression", "api", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_with_page_size_zero(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с "pageSize" равным 0.
        """
        with allure.step("Получение афиш фильмов"):
            filter_by_page_size = {"pageSize": 0}
            api_manager.movies_api.get_movies(filter_by_page_size, 400)

    @pytest.mark.regression
    @allure.story("Неуспешное получение афиш фильмов")
    @allure.title("Попытка получения афиш фильмов с отрицательным pageSize")
    @allure.tag("regression", "api", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_with_negative_page_size(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с отрицательным "pageSize".
        """
        with allure.step("Получение афиш фильмов"):
            filter_by_page_size = {"pageSize": -1}
            api_manager.movies_api.get_movies(filter_by_page_size, 400)

    @pytest.mark.regression
    @allure.story("Неуспешное получение афиш фильмов")
    @allure.title("Попытка получения афиш фильмов с  page равным 0")
    @allure.tag("regression", "api", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_with_page_zero(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с "page" равным 0.
        """
        with allure.step("Получение афиш фильмов"):
            filter_by_page = {"page": 0}
            api_manager.movies_api.get_movies(filter_by_page, 400)

    @pytest.mark.regression
    @allure.story("Неуспешное получение афиш фильмов")
    @allure.title("Попытка получения афиш фильмов с отрицательным page")
    @allure.tag("regression", "api", "negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_with_negative_page(self, api_manager: ApiManager) -> None:
        """
        Тест на получение афиш фильмов с отрицательным "page".
        """
        with allure.step("Получение афиш фильмов"):
            filter_by_page = {"page": -1}
            api_manager.movies_api.get_movies(filter_by_page, 400)
