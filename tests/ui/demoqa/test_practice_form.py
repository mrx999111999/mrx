from datetime import datetime

import allure
import pytest
from playwright.sync_api import Page
from pytest_check import check

from models.pages.demoqa.practice_form import DemoQAPracticeFormPage


@pytest.mark.ui
@allure.epic("https://demoqa.com")
@allure.feature("Forms")
class TestPracticeForm:
    @pytest.mark.smoke
    @allure.story("Practice Form")
    @allure.title("Регистрация студента с валидными данными")
    @allure.tag("smoke", "ui", "registration")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_student_registration_form(self, page: Page) -> None:
        """
        Тест на заполнение формы для регистрации студента
        """
        # Создаем объект класса DemoQAPracticeFormPage
        form_page = DemoQAPracticeFormPage(page)

        # Открытие страницы
        form_page.open()

        # Заполняем имя, фамилию и email
        form_page.enter_first_name('Ivan')
        form_page.enter_last_name('Ivanov')
        form_page.enter_email('test@test.com')

        # Выбираем пол
        form_page.select_male_gender()

        # Заполняем номер телефона
        form_page.enter_mobile('1234567891')

        # Проверка даты рождения по умолчанию
        date_of_birth_value = form_page.get_date_of_birth_value()
        today = datetime.now().strftime('%d %b %Y')
        with check:
            assert date_of_birth_value == today, f"Дата по умолчанию {date_of_birth_value} не совпадает с сегодняшней {today}"

        # Выбор предмета обучения
        form_page.enter_subject('Math')

        # Выбор хобби студента
        form_page.select_reading_hobby()

        # Заполнение адреса студента
        form_page.fill_current_address('Улица Пушкина, дом Колотушкина')

        # Выбор местоположения студента
        form_page.select_state('Uttar Pradesh')
        form_page.select_city('Lucknow')

        # Отправка формы
        form_page.submit_form()
        with check:
            assert form_page.is_submission_successful(), "Должно появиться модальное окно после отправки"

        # Проверка текста футера
        footer_text = form_page.get_footer_text()
        expected_footer = "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED."
        with check:
            assert footer_text == expected_footer, f"Текст футера '{footer_text}' не совпадает с ожидаемым '{expected_footer}'"
