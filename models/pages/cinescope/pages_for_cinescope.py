from playwright.sync_api import Page

from tests.ui.cinescope.base_page import BasePage


class CinescopRegisterPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = f"{self.home_url}register"

        # Поля формы регистрации
        self.full_name_input = "input[name='fullName']"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.repeat_password_input = "input[name='passwordRepeat']"

        # Кнопки для регистрации и входа
        self.register_button = "form button:has-text('Зарегистрироваться')"
        self.sign_button = "a[href='/login' and text()='Войти']"

    # Локальные action методы
    def open(self) -> None:
        """Открывает страницу регистрации"""
        self.open_url(self.url)

    def register(self, full_name: str, email: str, password: str, confirm_password: str) -> None:
        """Выполняет регистрацию пользователя"""
        self.enter_text_to_element(self.full_name_input, full_name)
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.repeat_password_input, confirm_password)

        self.click_element(self.register_button)

    def assert_was_redirect_to_login_page(self) -> None:
        """Проверяет редирект на страницу логина после регистрации"""
        self.wait_redirect_for_url(f"{self.home_url}login")

    def assert_allert_was_pop_up(self) -> None:
        """Проверяет появление алерта с текстом 'Подтвердите свою почту'"""
        self.check_pop_up_element_with_text("Подтвердите свою почту")


class CinescopLoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = f"{self.home_url}login"

        # Поля формы авторизации
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"

        # Кнопки для регистрации и входа
        self.login_button = "form button:has-text('Войти')"
        self.register_button = "a[href='/register' and text()='Зарегистрироваться']"

    # Локальные action методы
    def open(self) -> None:
        """Открывает страницу авторизации"""
        self.open_url(self.url)

    def login(self, email: str, password: str) -> None:
        """Выполняет авторизацию пользователя"""
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.email_input, email)

        self.click_element(self.login_button)

    def assert_was_redirect_to_home_page(self) -> None:
        """Проверяет редирект на домашнюю страницу после авторизации"""
        self.wait_redirect_for_url(self.home_url)

    def assert_alert_was_pop_up(self) -> None:
        """Проверяет появление алерта с текстом 'Вы вошли в аккаунт'"""
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")
