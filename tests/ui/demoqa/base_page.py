import allure
from playwright.sync_api import Page

from tests.ui.action_page import PageAction


class BasePage(PageAction):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.home_url = "https://demoqa.com/"

        # Общие локаторы для всех страниц на сайте
        self.home_button = "a[href='https://demoqa.com']"

    @allure.step("Переход на главную страницу, из шапки сайта")
    def go_to_home_page(self) -> None:
        self.click_element(self.home_button)
        self.wait_redirect_for_url(self.home_url)
