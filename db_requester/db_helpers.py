import allure
from sqlalchemy.orm import Session as SASession
from db_models.user import UserDBModel
from db_models.movie import MovieDBModel


class DBHelper:
    """
    Класс с методами для работы с БД в тестах
    """

    def __init__(self, db_session: SASession) -> None:
        self.db_session = db_session

    @allure.step("Создание тестового пользователя")
    def create_test_user(self, user_data: dict) -> UserDBModel:
        """Создает тестового пользователя"""
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    @allure.step("Получение пользователя по ID")
    def get_user_by_id(self, user_id: str) -> UserDBModel | None:
        """Получает пользователя по ID"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    @allure.step("Получение пользователя по email")
    def get_user_by_email(self, email: str) -> UserDBModel | None:
        """Получает пользователя по email"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).first()

    @allure.step("Проверка существования пользователя по email")
    def user_exists_by_email(self, email: str) -> bool:
        """Проверяет существование пользователя по email"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).count() > 0

    @allure.step("Удаление пользователя")
    def delete_user(self, user: UserDBModel) -> None:
        """Удаляет пользователя"""
        self.db_session.delete(user)
        self.db_session.commit()

    @allure.step("Очистка тестовых данных")
    def cleanup_test_data(self, objects_to_delete: list) -> None:
        """Очищает тестовые данные"""
        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

    @allure.step("Получение фильма по названию")
    def get_movie_by_name_from_db(self, name: str) -> MovieDBModel | None:
        """Получает фильм по названию"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.name == name).first()

    @allure.step("Получение фильма по ID")
    def get_movie_by_id_from_db(self, movie_id: int) -> MovieDBModel | None:
        """Получает фильм по ID"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.id == movie_id).first()

    @allure.step("Создание тестового фильма")
    def create_test_movie_in_db(self, movie_data: dict) -> MovieDBModel:
        """Создает тестовый фильм"""
        movie = MovieDBModel(**movie_data)
        self.db_session.add(movie)
        self.db_session.commit()
        self.db_session.refresh(movie)
        return movie

    @allure.step("Удаление фильма")
    def delete_movie_from_db(self, movie: MovieDBModel) -> None:
        """Удаляет фильм"""
        self.db_session.delete(movie)
        self.db_session.commit()
