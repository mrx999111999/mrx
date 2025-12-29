import allure
import pytest
from playwright.sync_api import Page

from models.pages.cinescope.pages_for_cinescope import CinescopRegisterPage
from utils.data_generator import DataGeneratorForAuthAPI


@pytest.mark.ui
@allure.epic("https://dev-cinescope.coconutqa.ru")
@allure.feature("Регистрация")
class TestRegisterPage:
    @pytest.mark.smoke
    @allure.story("Успешная регистрация на сайте")
    @allure.title("Регистрация с валидными данными")
    @allure.tag("smoke", "ui")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_register_by_ui(self, page: Page) -> None:
        # Генерируем тестовые данные
        random_email = DataGeneratorForAuthAPI.generate_random_email()
        random_name = DataGeneratorForAuthAPI.generate_random_full_name()
        random_password = DataGeneratorForAuthAPI.generate_random_password()

        # Создаем объект класса CinescopRegisterPage
        register_page = CinescopRegisterPage(page)

        # Переходим на страницу регистрации
        register_page.open()

        # Регистрируемся
        register_page.register(f"PlaywrightTest {random_name}", random_email, random_password,
                               random_password)

        # Проверяем редирект на страницу логина
        register_page.assert_was_redirect_to_login_page()

        # Скриншот для отчета (раскомментировать при необходимости)
        # register_page.make_screenshot_and_attach_to_allure()

        # Проверяем всплывающее уведомление
        register_page.assert_allert_was_pop_up()
