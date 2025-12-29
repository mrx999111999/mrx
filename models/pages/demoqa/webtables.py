from playwright.sync_api import Page

from tests.ui.demoqa.base_page import BasePage


class DemoQAWebTablesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}webtables"

        # Локаторы элементов
        self.add_button = "button:has-text('Add')"
        self.submit_button = "button:has-text('Submit')"
        self.search_box = "input[placeholder='Type to search']"

        self.first_name_input = "input[placeholder='First Name']"
        self.last_name_input = "input[placeholder='Last Name']"
        self.user_email_input = "input[placeholder='name@example.com']"
        self.age_input = "input[placeholder='Age']"
        self.salary_input = "input[placeholder='Salary']"
        self.department_input = "input[placeholder='Department']"

    # Локальные action методы
    def open(self) -> None:
        """Открывает страницу с таблицами"""
        self.open_url(self.url)

    def click_add_button(self) -> None:
        """Нажимает кнопку 'Add' для открытия формы регистрации"""
        self.click_element(self.add_button)

    def fill_registration_form(self, first_name: str, last_name: str, email: str,
                               age: str, salary: str, department: str) -> None:
        """Заполняет форму регистрации пользователя"""
        self.enter_text_to_element(self.first_name_input, first_name)
        self.enter_text_to_element(self.last_name_input, last_name)
        self.enter_text_to_element(self.user_email_input, email)
        self.enter_text_to_element(self.age_input, age)
        self.enter_text_to_element(self.salary_input, salary)
        self.enter_text_to_element(self.department_input, department)

    def click_submit_button(self) -> None:
        """Нажимает кнопку 'Submit' для отправки формы"""
        self.click_element(self.submit_button)

    def search_in_table(self, search_text: str) -> None:
        """Выполняет поиск в таблице по указанному тексту"""
        self.enter_text_to_element(self.search_box, search_text)

    def is_registration_form_visible(self) -> bool:
        """Проверяет видимость формы регистрации"""
        return self.is_element_visible('.modal-header:has-text("Registration Form")')
