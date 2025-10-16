import requests
import pytest
from requests import Session
from sqlalchemy.orm import Session as SASession
from typing import Generator, Callable

from db_models.user import UserDBModel
from db_requester.db_client import get_db_session
from models.models import UserRegisterRequest, CreateMovieRequest, UserRegisterResponse, CreateMovieResponse
from utils.data_generator import DataGeneratorForAuthAPI, DataGeneratorForMoviesAPI
from api.api_manager import ApiManager
from entities.user import User
from resources.user_creds import SuperAdminCreds
from enums.roles import Roles
from db_requester.db_helpers import DBHelper
from utils.tools import Tools

DEFAULT_UI_TIMEOUT = 100000  # Пример значения таймаута


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
def registered_user(api_manager: ApiManager, test_user: UserRegisterRequest) -> UserRegisterResponse:
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = api_manager.auth_api.register_user(test_user).json()
    registered_user = UserRegisterResponse(**response)

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
    user_data.email = DataGeneratorForAuthAPI.generate_random_email()
    user_data.password = DataGeneratorForAuthAPI.generate_random_password()
    user_data.fullName = DataGeneratorForAuthAPI.generate_random_full_name()

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
    super_admin.api.user_api.update_user(response["id"], {"roles": ["ADMIN"]})
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user


@pytest.fixture(scope="function")
def test_movie() -> CreateMovieRequest:
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

    return CreateMovieRequest(
        name=random_name,
        imageUrl=random_image_url,
        price=random_price,
        description=random_description,
        location=random_location,
        published=random_published,
        genreId=random_genre_id
    )


@pytest.fixture(scope="function")
def created_movie(super_admin: User, test_movie: CreateMovieRequest) -> CreateMovieResponse:
    """
    Фикстура для создания фильма.
    """
    response = super_admin.api.movies_api.create_movie(test_movie).json()
    created_movie = CreateMovieResponse(**response)
    return created_movie


@pytest.fixture(scope="module")
def db_session() -> Generator[SASession, None, None]:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()


@pytest.fixture(scope="function")
def db_helper(db_session: SASession) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    database_helper = DBHelper(db_session)
    return database_helper


@pytest.fixture(scope="function")
def created_test_user(db_helper: DBHelper) -> Generator[UserDBModel, None, None]:
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGeneratorForAuthAPI.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)


@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False, channel="chrome")
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir('playwright_trace', log_name)
    context.tracing.stop(path=trace_path)
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()
