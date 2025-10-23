import allure
from playwright.sync_api import Page


class PageAction:
    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str) -> None:
        self.page.goto(url)

    @allure.step("Ввод текста '{text}' в поле '{locator}'")
    def enter_text_to_element(self, locator: str, text: str) -> None:
        self.page.fill(locator, text)

    @allure.step("Клик по элементу '{locator}'")
    def click_element(self, locator: str) -> None:
        self.page.click(locator)

    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_redirect_for_url(self, url: str) -> None:
        self.page.wait_for_url(url)
        assert self.page.url == url, "Редирект на домашнюю старницу не произошел"

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator: str) -> str:
        return self.page.locator(locator).text_content()

    @allure.step("Ожидание появления или исчезновения элемента: {locator}, state = {state}")
    def wait_for_element(self, locator: str, state: str = "visible") -> None:
        self.page.locator(locator).wait_for(state=state)

    @allure.step("Скриншот текущей страницы")
    def make_screenshot_and_attach_to_allure(self) -> None:
        screenshot_path = "screenshot.png"
        self.page.screenshot(path=screenshot_path, full_page=True)  # full_page=True для скриншота всей страницы

        # Прикрепление скриншота к Allure-отчёту
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot after redirect", attachment_type=allure.attachment_type.PNG)

    @allure.step("Проверка всплывающего сообщения c текстом: {text}")
    def check_pop_up_element_with_text(self, text: str) -> None:
        with allure.step("Проверка появления алерта с текстом: '{text}'"):
            notification_locator = self.page.get_by_text(text)
            # Ждем появления элемента
            notification_locator.wait_for(state="visible")
            assert notification_locator.is_visible(), "Уведомление не появилось"

        with allure.step("Проверка исчезновения алерта с текстом: '{text}'"):
            # Ждем, пока алерт исчезнет
            notification_locator.wait_for(state="hidden")
            assert not notification_locator.is_visible(), "Уведомление не исчезло"

    @allure.step("Проверка видимости элемента: {locator}")
    def is_element_visible(self, locator: str) -> bool:
        """Проверяет, виден ли элемент на странице"""
        return self.page.locator(locator).is_visible()

    @allure.step("Проверка активности элемента: {locator}")
    def is_element_enabled(self, locator: str) -> bool:
        """Проверяет, активен ли элемент для взаимодействия"""
        return self.page.locator(locator).is_enabled()

    @allure.step("Проверка выбранного состояния: {locator}")
    def is_element_checked(self, locator: str) -> bool:
        """Проверяет, выбран ли элемент (чекбокс, радио-кнопка)"""
        return self.page.locator(locator).is_checked()
