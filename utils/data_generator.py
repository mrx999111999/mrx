import datetime
import random
import string

from faker import Faker

faker = Faker()


class DataGeneratorForAuthAPI:

    @staticmethod
    def generate_random_email() -> str:
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_full_name() -> str:
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password() -> str:
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGeneratorForAuthAPI.generate_random_email(),
            'full_name': DataGeneratorForAuthAPI.generate_random_full_name(),
            'password': DataGeneratorForAuthAPI.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }


class DataGeneratorForMoviesAPI:

    @staticmethod
    def generate_random_name() -> str:
        return f"{faker.catch_phrase()}"

    @staticmethod
    def generate_random_image_url() -> str:
        return f"{faker.image_url()}"

    @staticmethod
    def generate_random_price() -> int:
        return random.randint(100, 2000)

    @staticmethod
    def generate_random_description() -> str:
        return f"{faker.text(max_nb_chars=200)}"

    @staticmethod
    def generate_random_location() -> str:
        return random.choice(["SPB", "MSK"])

    @staticmethod
    def generate_random_published() -> bool:
        return random.choice([True, False])

    @staticmethod
    def generate_random_genre_id() -> int:
        return random.randint(1, 10)
