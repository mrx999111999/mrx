from playwright.sync_api import Page
from tests.ui.demoqa.base_page import BasePage


class DemoQACheckboxPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = f"{self.home_url}checkbox"

        # Кнопки управления деревом
        self.expand_all_button = "button[title='Expand all']"
        self.collapse_all_button = "button[title='Collapse all']"
        self.home_toggle = "button[title='Toggle']"

        # Чекбоксы элементов
        self.home_checkbox = "label[for='tree-node-home']"
        self.desktop_checkbox = "label[for='tree-node-desktop']"
        self.documents_checkbox = "label[for='tree-node-documents']"
        self.downloads_checkbox = "label[for='tree-node-downloads']"

    def open(self) -> None:
        """Открывает страницу с чекбоксами"""
        self.open_url(self.url)

    def click_expand_all(self) -> None:
        """Нажимает кнопку 'Expand all'"""
        self.click_element(self.expand_all_button)

    def click_collapse_all(self) -> None:
        """Нажимает кнопку 'Collapse all'"""
        self.click_element(self.collapse_all_button)

    def click_home_toggle(self) -> None:
        """Кликает по тогглу Home"""
        self.click_element(self.home_toggle)

    def select_home_checkbox(self) -> None:
        """Выбирает чекбокс 'Home'"""
        self.click_element(self.home_checkbox)

    def select_desktop_checkbox(self) -> None:
        """Выбирает чекбокс 'Desktop'"""
        self.click_element(self.desktop_checkbox)

    def select_documents_checkbox(self) -> None:
        """Выбирает чекбокс 'Documents'"""
        self.click_element(self.documents_checkbox)

    def select_downloads_checkbox(self) -> None:
        """Выбирает чекбокс 'Downloads'"""
        self.click_element(self.downloads_checkbox)

    def is_home_checkbox_visible(self) -> bool:
        """Проверяет видимость чекбокса 'Home'"""
        return self.is_element_visible(self.home_checkbox)

    def is_desktop_checkbox_visible(self) -> bool:
        """Проверяет видимость чекбокса 'Desktop'"""
        return self.is_element_visible(self.desktop_checkbox)

    def is_documents_checkbox_visible(self) -> bool:
        """Проверяет видимость чекбокса 'Documents'"""
        return self.is_element_visible(self.documents_checkbox)

    def is_downloads_checkbox_visible(self) -> bool:
        """Проверяет видимость чекбокса 'Downloads'"""
        return self.is_element_visible(self.downloads_checkbox)
