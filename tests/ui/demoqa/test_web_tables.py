import allure
import pytest
from playwright.sync_api import Page
from pytest_check import check

from models.pages.demoqa.webtables import DemoQAWebTablesPage


@pytest.mark.ui
@allure.epic("https://demoqa.com")
@allure.feature("Elements")
class TestWebTables:
    @pytest.mark.smoke
    @allure.story("Web Tables")
    @allure.title("Регистрация сотрудника с валидными данными")
    @allure.tag("smoke", "ui")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_registration_form_web_tables(self, page: Page) -> None:
        """
        Тест на заполнение формы для регистрации работника
        """
        # Создаем объект класса DemoQAWebTablesPage
        web_tables_page = DemoQAWebTablesPage(page)

        # Открытие страницы
        web_tables_page.open()

        # Клик по кнопке Add и проверка появления формы для регистрации
        web_tables_page.click_add_button()
        with check:
            assert web_tables_page.is_registration_form_visible(), "Форма регистрации должна появиться после клика на Add"

        # Заполнение формы регистрации
        web_tables_page.fill_registration_form(
            first_name="Ivan",
            last_name="Ivanov",
            email="test@test.com",
            age="28",
            salary="100000",
            department="IT"
        )

        # Клик по кнопке Submit
        web_tables_page.click_submit_button()

        # Проверки результата
        page.wait_for_timeout(2000)
        with check:
            assert not web_tables_page.is_registration_form_visible(), "Форма должна закрыться после отправки"
