import allure
import pytest
from playwright.sync_api import Page
from pytest_check import check

from models.pages.demoqa.radio_button import DemoQARadioButtonPage


@pytest.mark.ui
@allure.epic("https://demoqa.com")
@allure.feature("Elements")
class TestRadioButton:
    @pytest.mark.smoke
    @allure.story("Radio Button")
    @allure.title("Проверка активности радиобаттонов")
    @allure.tag("smoke", "ui")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_radio_buttons_initial_state_and_selection(self, page: Page) -> None:
        """
        Тест на проверку активности и выбора радиобаттонов
        """
        # Создаем объект класса DemoQARadioButtonPage
        radio_page = DemoQARadioButtonPage(page)

        # Открытие страницы
        radio_page.open()

        # Проверка состояния радиобаттонов
        with check:
            assert radio_page.is_yes_radio_enabled(), "Радио-кнопка Yes должна быть доступна"
            assert radio_page.is_impressive_radio_enabled(), "Радио-кнопка Impressive должна быть доступна"
            assert not radio_page.is_no_radio_enabled(), "Радио-кнопка No должна быть недоступна"

        # Выбираем радиобаттон Yes и проверяем, что он действительно выбран
        radio_page.select_yes_radio()
        with check:
            assert radio_page.is_yes_radio_checked(), "Радио-кнопка Yes должна быть выбрана после клика"
            assert not radio_page.is_impressive_radio_checked(), "Impressive не должна быть выбрана"
