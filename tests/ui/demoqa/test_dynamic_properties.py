import allure
import pytest
from playwright.sync_api import Page
from pytest_check import check

from models.pages.demoqa.dynamic_properties import DemoQADynamicPropertiesPage


@pytest.mark.ui
@allure.epic("https://demoqa.com")
@allure.feature("Elements")
class TestDynamicProperties:
    @pytest.mark.smoke
    @allure.story("Dynamic Properties")
    @allure.title("Проверка появления элемента")
    @allure.tag("smoke", "ui")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_element_appears_after_5_seconds(self, page: Page) -> None:
        """
        Тест на проверку появления элемента
        """
        # Создаем объект класса DemoQADynamicPropertiesPage
        dynamic_page = DemoQADynamicPropertiesPage(page)

        # Открытие страницы
        dynamic_page.open()

        # Проверка, что элемента изначально нет на странице
        with check:
            assert not dynamic_page.is_visible_after_button_visible(), "Кнопка не должна быть видна изначально"

        # Ожидание появления элемента
        dynamic_page.wait_for_visible_after_button()

        # Проверка, что элемент теперь виден
        with check:
            assert dynamic_page.is_visible_after_button_visible(), "Кнопка должна стать видимой после ожидания"
