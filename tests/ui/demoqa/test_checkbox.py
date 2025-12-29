import allure
import pytest
from playwright.sync_api import Page
from pytest_check import check

from models.pages.demoqa.checkbox import DemoQACheckboxPage


@pytest.mark.ui
@allure.epic("https://demoqa.com")
@allure.feature("Elements")
class TestCheckbox:
    @pytest.mark.smoke
    @allure.story("Check Box")
    @allure.title("Проверка видимости чекбоксов")
    @allure.tag("smoke", "ui")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_box_are_visible(self, page: Page) -> None:
        """
        Тест на проверку видимости чекбоксов
        """
        # Создаем объект класса DemoQACheckboxPage
        checkbox_page = DemoQACheckboxPage(page)

        # Открытие страницы
        checkbox_page.open()

        # Проверка, что чекбокс Home виден, а Desktop нет
        with check:
            assert checkbox_page.is_home_checkbox_visible(), "Чекбокс Home должен быть виден"
            assert not checkbox_page.is_desktop_checkbox_visible(), "Чекбокс Desktop должен быть скрыт до раскрытия"

        # Клик по тогглу для раскрытия списка
        checkbox_page.click_home_toggle()

        # Проверка, что Desktop стал виден после раскрытия
        with check:
            assert checkbox_page.is_desktop_checkbox_visible(), "Desktop должен стать видимым после раскрытия"
