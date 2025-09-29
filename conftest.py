import requests
import pytest
from requests import Session
from typing import Any, Generator, Callable
from db_requester.db_client import get_db_session
from constants import REGISTER_ENDPOINT, MOVIES_ENDPOINT, USER_ENDPOINT
from models.test_user import UserRegisterRequest
from utils.data_generator import DataGeneratorForAuthAPI, DataGeneratorForMoviesAPI
from api.api_manager import ApiManager
from entities.user import User
from resources.user_creds import SuperAdminCreds
from enums.roles import Roles
from db_requester.db_helpers import DBHelper


@pytest.fixture(scope="function")
def test_user() -> UserRegisterRequest:
    """
    Фикстура подготавливает данные для регистрации пользователя.
    """
    random_email = DataGeneratorForAuthAPI.generate_random_email()
    random_name = DataGeneratorForAuthAPI.generate_random_full_name()
    random_password = DataGeneratorForAuthAPI.generate_random_password()

    return UserRegisterRequest(
        email=random_email,
        fullName=random_name,
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )


@pytest.fixture(scope="function")
def creation_user_data(test_user: UserRegisterRequest) -> UserRegisterRequest:
    """
    Фикстура подготавливает данные для создания пользователя.
    """
    return test_user.model_copy(update={"verified": True, "banned": False})


@pytest.fixture(scope="function")
def registered_user(api_manager: ApiManager, test_user: UserRegisterRequest) -> dict[str, Any]:
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = api_manager.auth_api.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    ).json()
    registered_user = test_user.model_dump()
    registered_user["id"] = response["id"]
    return registered_user


@pytest.fixture(scope="session")
def session() -> Generator[Session, None, None]:
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session: Session) -> ApiManager:
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture
def user_session() -> Generator[Callable[[], ApiManager], None, None]:
    """
    Фикстура для управления жизненным циклом пользовательских сессий для API-тестов.
    """
    user_pool = []

    def _create_user_session() -> ApiManager:
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session: Callable[[], ApiManager]) -> User:
    """
    Фикстура для получения пользователя с ролью SUPER_ADMIN.
    """
    new_session = user_session()

    super_admin_user = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin_user.api.auth_api.authenticate(super_admin_user.creds)
    return super_admin_user


@pytest.fixture
def common(user_session: Callable[[], ApiManager], super_admin: User, creation_user_data: UserRegisterRequest) -> User:
    """
    Фикстура создает обычного пользователя через суперадмина.
    """
    user_data = creation_user_data.model_copy()
    new_session = user_session()

    common_user = User(
        user_data.email,
        user_data.password,
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin(user_session: Callable[[], ApiManager], super_admin: User, creation_user_data: UserRegisterRequest) -> User:
    """
    Фикстура создает обычного пользователя через суперадмина и повышает его роль до ADMIN через PATCH.
    """
    admin_data = creation_user_data.model_copy()
    admin_data.email = DataGeneratorForAuthAPI.generate_random_email()
    admin_data.password = DataGeneratorForAuthAPI.generate_random_password()
    admin_data.fullName = DataGeneratorForAuthAPI.generate_random_full_name()

    new_session = user_session()

    admin_user = User(
        admin_data.email,
        admin_data.password,
        [Roles.ADMIN.value],
        new_session)

    response = super_admin.api.user_api.create_user(admin_data).json()
    super_admin.api.auth_api.send_request(
        method="PATCH",
        endpoint=f'{USER_ENDPOINT}/{response["id"]}',
        data={"roles": ["ADMIN"]})
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user


@pytest.fixture(scope="function")
def test_movie() -> dict[str, str | int | float | bool]:
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


@pytest.fixture(scope="function")
def created_movie(super_admin: User, test_movie: dict[str, str | int | float | bool]) -> dict[
    str, str | int | float | bool]:
    """
    Фикстура для создания фильма.
    """
    response = super_admin.api.movies_api.send_request(
        method="POST",
        endpoint=MOVIES_ENDPOINT,
        data=test_movie,
        expected_status=201
    )
    response_data = response.json()
    created_movie = test_movie.copy()
    created_movie["id"] = response_data["id"]
    return created_movie


@pytest.fixture(scope="module")
def db_session() -> Generator[Session, None, None]:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()


@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    database_helper = DBHelper(db_session)
    return database_helper


@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGeneratorForAuthAPI.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)
