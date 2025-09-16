import requests
import pytest
from constants import REGISTER_ENDPOINT, MOVIES_ENDPOINT
from utils.data_generator import DataGeneratorForAuthAPI, DataGeneratorForMoviesAPI
from api.api_manager import ApiManager


@pytest.fixture(scope="session")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGeneratorForAuthAPI.generate_random_email()
    random_name = DataGeneratorForAuthAPI.generate_random_full_name()
    random_password = DataGeneratorForAuthAPI.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture(scope="session")
def registered_user(api_manager: ApiManager, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = api_manager.auth_api.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture(scope="session")
def test_movie():
    """
    Генерация случайного фильма для тестов.
    """
    random_name = DataGeneratorForMoviesAPI.generate_random_name()
    random_image_url = DataGeneratorForMoviesAPI.generate_random_image_url()
    random_price = DataGeneratorForMoviesAPI.generate_random_price()
    random_description = DataGeneratorForMoviesAPI.generate_random_description()
    random_location = DataGeneratorForMoviesAPI.generate_random_location()
    random_published = DataGeneratorForMoviesAPI.generate_random_published()
    random_genre_id = DataGeneratorForMoviesAPI.generate_random_genre_id()

    return {
        "name": random_name,
        "imageUrl": random_image_url,
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": random_published,
        "genreId": random_genre_id
    }


@pytest.fixture(scope="session")
def created_movie(api_manager: ApiManager, test_movie):
    """
    Фикстура для создания фильма.
    """
    response = api_manager.movies_api.send_request(
        method="POST",
        endpoint=MOVIES_ENDPOINT,
        data=test_movie,
        expected_status=201
    )
    response_data = response.json()
    created_movie = test_movie.copy()
    created_movie["id"] = response_data["id"]
    return created_movie
