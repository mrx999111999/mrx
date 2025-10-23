from playwright.sync_api import Page
from tests.ui.demoqa.base_page import BasePage


class DemoQAPracticeFormPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = f"{self.home_url}automation-practice-form"

        # Локаторы для First Name, Last Name, Email, Mobile
        self.first_name = "input[placeholder='First Name']"
        self.last_name = "input[placeholder='Last Name']"
        self.email = "input[placeholder='name@example.com']"
        self.mobile = "input[placeholder='Mobile Number']"

        # Радиобаттоны для выбора пола
        self.gender_male = "label[for='gender-radio-1']"
        self.gender_female = "label[for='gender-radio-2']"
        self.gender_other = "label[for='gender-radio-3']"

        # Поле для даты рождения
        self.date_of_birth = "input#dateOfBirthInput"

        # Поле для предметов
        self.subjects = "#subjectsInput"

        # Кнопка для загрузки файла
        self.upload_picture = "input#uploadPicture"

        # Чекбоксы для выбора хобби
        self.hobbies_sports = "label[for='hobbies-checkbox-1']"
        self.hobbies_reading = "label[for='hobbies-checkbox-2']"
        self.hobbies_music = "label[for='hobbies-checkbox-3']"

        # Поле для текущего адреса
        self.current_address = "textarea#currentAddress"

        # Выпадающие списки штата и города
        self.state_dropdown = "div#state"
        self.city_dropdown = "div#city"

        # Кнопка для отправки формы
        self.submit_button = "button#submit"

        # Модальное окно
        self.modal_content = "div.modal-content"

    def open(self) -> None:
        """Открытие страницы с формой"""
        self.open_url(self.url)

    def enter_first_name(self, name: str) -> None:
        """Заполнение поля First Name"""
        self.enter_text_to_element(self.first_name, name)

    def enter_last_name(self, name: str) -> None:
        """Заполнение поля Last Name"""
        self.enter_text_to_element(self.last_name, name)

    def enter_email(self, email: str) -> None:
        """Заполнение поля Email"""
        self.enter_text_to_element(self.email, email)

    def enter_mobile(self, mobile: str) -> None:
        """Заполнение поля Mobile"""
        self.enter_text_to_element(self.mobile, mobile)

    def select_male_gender(self) -> None:
        """Выбор мужского пола"""
        self.click_element(self.gender_male)

    def select_female_gender(self) -> None:
        """Выбор женского пола"""
        self.click_element(self.gender_female)

    def select_other_gender(self) -> None:
        """Выбор варианта 'Other' для пола"""
        self.click_element(self.gender_other)

    def fill_current_address(self, address: str) -> None:
        """Заполнение поля текущего адреса"""
        self.enter_text_to_element(self.current_address, address)

    def submit_form(self) -> None:
        """Нажатие кнопки отправки формы"""
        self.click_element(self.submit_button)

    def enter_subject(self, subject: str) -> None:
        """Заполнение поля Subjects с нажатием клавиши Enter"""
        self.enter_text_to_element(self.subjects, subject)
        self.page.keyboard.press('Enter')

    def select_sports_hobby(self) -> None:
        """Выбор чекбокса Sports"""
        self.click_element(self.hobbies_sports)

    def select_reading_hobby(self) -> None:
        """Выбор чекбокса Reading"""
        self.click_element(self.hobbies_reading)

    def select_music_hobby(self) -> None:
        """Выбор чекбокса Music"""
        self.click_element(self.hobbies_music)

    def select_state(self, state_name: str) -> None:
        """Выбор штата из выпадающего списка"""
        self.click_element(self.state_dropdown)
        self.click_element(f"text={state_name}")

    def select_city(self, city_name: str) -> None:
        """Выбор города из выпадающего списка"""
        self.click_element(self.city_dropdown)
        self.click_element(f"text={city_name}")

    def get_footer_text(self) -> str:
        """Возвращает текст футера"""
        return self.page.inner_text('footer')

    def get_date_of_birth_value(self) -> str:
        """Возвращает значение поля даты рождения"""
        return self.page.get_attribute(self.date_of_birth, 'value')

    def is_submission_successful(self) -> bool:
        """Проверяет успешность отправки формы по наличию модального окна"""
        return self.is_element_visible(self.modal_content)
