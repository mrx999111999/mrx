from playwright.sync_api import Page

from tests.ui.demoqa.base_page import BasePage


class DemoQARadioButtonPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}radio-button"

        # Локаторы элементов
        self.yes_radio = "label[for='yesRadio']"
        self.impressive_radio = "label[for='impressiveRadio']"
        self.no_radio = "label[for='noRadio']"

    def open(self) -> None:
        """Открывает страницу с радио-кнопками"""
        self.open_url(self.url)

    def is_yes_radio_enabled(self) -> bool:
        """Проверяет, доступна ли радио-кнопка 'Yes'"""
        return self.is_element_enabled(self.yes_radio)

    def is_impressive_radio_enabled(self) -> bool:
        """Проверяет, доступна ли радио-кнопка 'Impressive'"""
        return self.is_element_enabled(self.impressive_radio)

    def is_no_radio_enabled(self) -> bool:
        """Проверяет, доступна ли радио-кнопка 'No'"""
        return self.is_element_enabled(self.no_radio)

    def is_yes_radio_checked(self) -> bool:
        """Проверяет, выбрана ли радио-кнопка 'Yes'"""
        return self.is_element_checked(self.yes_radio)

    def is_impressive_radio_checked(self) -> bool:
        """Проверяет, выбрана ли радио-кнопка 'Impressive'"""
        return self.is_element_checked(self.impressive_radio)

    def select_yes_radio(self) -> None:
        """Выбирает радио-кнопку 'Yes'"""
        self.click_element(self.yes_radio)

    def select_impressive_radio(self) -> None:
        """Выбирает радио-кнопку 'Impressive'"""
        self.click_element(self.impressive_radio)
