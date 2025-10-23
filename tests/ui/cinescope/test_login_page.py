import allure
import pytest
from playwright.sync_api import Page

from models.models import UserRegisterRequest, UserRegisterResponse
from models.pages.cinescope.pages_for_cinescope import CinescopLoginPage


@pytest.mark.ui
@allure.epic("https://dev-cinescope.coconutqa.ru")
@allure.feature("Авторизация")
class TestLoginPage:
    @pytest.mark.smoke
    @allure.story("Успешная авторизация на сайте")
    @allure.title("Авторизация с валидными данными")
    @allure.tag("smoke", "ui")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_by_ui(self, page: Page, registered_user: UserRegisterResponse,
                         test_user: UserRegisterRequest) -> None:
        # Создаем объект класса CinescopLoginPage
        login_page = CinescopLoginPage(page)

        # Переходим на страницу авторизации
        login_page.open()

        # Авторизуемся
        login_page.login(registered_user.email, test_user.password)

        # Проверяем редирект на главную страницу
        login_page.assert_was_redirect_to_home_page()

        # Скриншот для отчета (раскомментировать при необходимости)
        # login_page.make_screenshot_and_attach_to_allure()

        # Проверяем всплывающее уведомление
        login_page.assert_allert_was_pop_up()
