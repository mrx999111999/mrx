from playwright.sync_api import Page
from tests.ui.demoqa.base_page import BasePage


class DemoQADynamicPropertiesPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = f"{self.home_url}dynamic-properties"

        # Кнопки с динамическими свойствами
        self.enable_after_button = "button#enableAfter"
        self.color_change_button = "button#colorChange"
        self.visible_after_button = "button#visibleAfter"

    def open(self) -> None:
        """Открывает страницу с динамическими свойствами"""
        self.open_url(self.url)

    def wait_for_visible_after_button(self) -> None:
        """Ждет пока кнопка 'Visible After 5 Seconds' станет видимой"""
        self.wait_for_element(self.visible_after_button, state="visible")

    def wait_for_enable_after_button(self) -> None:
        """Ждет пока кнопка 'Will enable 5 seconds' станет активной"""
        self.wait_for_element(self.enable_after_button, state="enabled")

    def is_visible_after_button_visible(self) -> bool:
        """Проверяет видимость кнопки 'Visible After 5 Seconds'"""
        return self.is_element_visible(self.visible_after_button)