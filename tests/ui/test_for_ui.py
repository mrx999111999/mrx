from datetime import datetime

import allure
import pytest
from playwright.sync_api import Page
from pytest_check import check


@pytest.mark.ui
@allure.epic("https://demoqa.com")
@allure.feature("Elements")
class TestForElements:
    @pytest.mark.smoke
    @allure.story("Web Tables")
    @allure.title("Регистрация сотрудника с валидными данными")
    @allure.tag("smoke", "ui", "registration")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_registration_form_web_tables(self, page: Page) -> None:
        """
        Тест на заполнение формы для регистрации работника
        """
        with allure.step("Открытие страницы https://demoqa.com/webtables"):
            page.goto("https://demoqa.com/webtables")

        with allure.step("Клик по кнопке Add"):
            page.locator('button:has-text("Add")').click()

        with allure.step("Проверка, что форма регистрации открылась"):
            with check:
                assert page.locator('.modal-header:has-text("Registration Form")').is_visible(timeout=5000)

        with allure.step("Заполнение полей"):
            page.locator('input[placeholder="First Name"]').fill("Ivan")
            page.locator('input[placeholder="Last Name"]').fill("Ivanov")
            page.locator('input[placeholder="name@example.com"]').fill("test@test.com")
            page.locator('input[placeholder="Age"]').fill("28")
            page.locator('input[placeholder="Salary"]').fill("100000")
            page.locator('input[placeholder="Department"]').fill("IT")

        with allure.step("Клик по кнопке Submit"):
            page.locator('button:has-text("Submit")').click()

    @pytest.mark.smoke
    @allure.story("Radio Button")
    @allure.title("Проверка активности радиобаттонов")
    @allure.tag("smoke", "ui")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_radio_buttons_are_enabled(self, page: Page) -> None:
        """
        Тест на проверку активности радиобаттнов
        """
        with allure.step("Открытие страницы https://demoqa.com/radio-button"):
            page.goto("https://demoqa.com/radio-button")

        with allure.step("Проверка, что радиобаттоны Yes и Impressive активны, а No неактивен"):
            with check:
                assert page.is_enabled('#yesRadio')
                assert page.is_enabled('#impressiveRadio')
                assert not page.is_enabled('#noRadio')

    @pytest.mark.smoke
    @allure.story("Check Box")
    @allure.title("Проверка видимости чекбоксов")
    @allure.tag("smoke", "ui")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_box_are_visible(self, page: Page) -> None:
        """
        Тест на проверку видимости чекбоксов
        """
        with allure.step("Открытие страницы https://demoqa.com/checkbox"):
            page.goto("https://demoqa.com/checkbox")

        with allure.step("Проверка, что чекбокс Home виден, а Desktop нет"):
            with check:
                assert page.is_visible('label[for="tree-node-home"]')
                assert not page.is_visible('label[for="tree-node-desktop"]')

        with allure.step("Клик по тогглу для раскрытия списка"):
            page.locator('button[title="Toggle"]').click()

        with allure.step("Проверка, что Desktop стал виден после раскрытия"):
            with check:
                assert page.is_visible('label[for="tree-node-desktop"]')

    @pytest.mark.smoke
    @allure.story("Dynamic Properties")
    @allure.title("Проверка появления элемента")
    @allure.tag("smoke", "ui")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_element_appears_after_5_seconds(self, page: Page) -> None:
        """
        Тест на проверку появления элемента
        """
        with allure.step("Открытие страницы https://demoqa.com/dynamic-properties"):
            page.goto("https://demoqa.com/dynamic-properties")

        with allure.step("Проверка, что элемента изначально нет на странице"):
            with check:
                assert not page.is_visible('#visibleAfter')

        with allure.step("Ожидание появления элемента"):
            page.wait_for_selector('#visibleAfter', timeout=10000)

        with allure.step("Проверка, что элемент теперь виден"):
            with check:
                assert page.is_visible('#visibleAfter')


@pytest.mark.ui
@allure.epic("https://demoqa.com")
@allure.feature("Forms")
class TestForForms:
    @pytest.mark.smoke
    @allure.story("Practice Form")
    @allure.title("Регистрация студента с валидными данными")
    @allure.tag("smoke", "ui", "registration")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_student_registration_form(self, page: Page) -> None:
        """
        Тест на заполнение формы для регистрации студента
        """
        with allure.step("Открытие страницы https://demoqa.com/automation-practice-form"):
            page.goto('https://demoqa.com/automation-practice-form')

        with allure.step("Заполняем имя, фамилию и email"):
            page.fill('input[placeholder="First Name"]', 'Ivan')
            page.fill('input[placeholder="Last Name"]', 'Ivanov')
            page.fill('input[placeholder="name@example.com"]', 'test@test.com')

        with allure.step("Выбираем пол"):
            page.click('label[for="gender-radio-1"]')

        with allure.step("Заполняем номер телефона с имитацией печати"):
            page.type('input[placeholder="Mobile Number"]', '1234567891')

        with allure.step("Проверка даты рождения по умолчанию"):
            date_of_birth_value = page.get_attribute('#dateOfBirthInput', 'value')
            today = datetime.now().strftime('%d %b %Y')
            with check:
                assert date_of_birth_value == today, f"Дата по умолчанию {date_of_birth_value} не совпадает с сегодняшней {today}"

        with allure.step("Выбор предмета обучения"):
            page.fill('#subjectsInput', 'Math')
            page.keyboard.press('Enter')

        with allure.step("Выбор хобби студента"):
            page.click('label[for="hobbies-checkbox-2"]')

        with allure.step("Заполнение адреса студента"):
            page.fill('textarea#currentAddress', 'Улица Пушкина, дом Колотушкина')

        with allure.step("Выбор местоположения студента"):
            page.click('#state')
            page.click('text=Uttar Pradesh')
            page.click('#city')
            page.click('text=Lucknow')

        with allure.step("Проверка текста футера"):
            footer_text = page.inner_text('footer')
            expected_footer = "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED."
            assert footer_text == expected_footer, f"Текст футера '{footer_text}' не совпадает с ожидаемым '{expected_footer}'"
