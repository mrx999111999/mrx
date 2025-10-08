from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, List
from enums.roles import Roles
import datetime
import re


# Модели для Auth API
class UserRegisterRequest(BaseModel):
    email: str = Field(min_length=1, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                       description="Email адрес пользователя")
    fullName: str = Field(min_length=1, description="Полное имя пользователя")
    password: str = Field(min_length=8, max_length=20, description="Пароль пользователя")
    passwordRepeat: str = Field(min_length=8, max_length=20, description="Повтор пароля для подтверждения")
    roles: list[Roles] = Field(min_length=1, description="Роли пользователя")
    banned: bool | None = None
    verified: bool | None = None

    @classmethod
    @field_validator("password")
    def validate_password_strength(cls, value: str) -> str:
        """Валидация сложности пароля по требованиям"""

        # Проверка длины пароля
        if len(value) < 8 or len(value) > 20:
            raise ValueError("Пароль должен быть от 8 до 20 символов")

        # Проверка на минимум 1 букву
        if not re.search(r'[a-zA-Z]', value):
            raise ValueError("Пароль должен содержать минимум 1 букву")

        # Проверка на минимум 1 цифру
        if not re.search(r'\d', value):
            raise ValueError("Пароль должен содержать минимум 1 цифру")

        # Проверка на допустимые символы
        if not re.match(r'^[a-zA-Z0-9?@#$%^&*|:]+$', value):
            raise ValueError("Пароль содержит недопустимые символы. "
                             "Допустимы: буквы, цифры, ?@#$%^&*|:")

        return value

    @classmethod
    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, values) -> str:
        if "password" in values.data and value != values.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value


class UserRegisterResponse(BaseModel):
    id: str = Field(min_length=1, description="Уникальный идентификатор пользователя")
    email: str = Field(min_length=1, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                       description="Email адрес пользователя")
    fullName: str = Field(min_length=1, description="Полное имя пользователя")
    verified: bool
    banned: bool
    roles: list[Roles] = Field(min_length=1, description="Роли пользователя")
    createdAt: str = Field(min_length=1, description="Дата и время создания пользователя в формате ISO 8601")

    @classmethod
    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value


class UserLoginRequest(BaseModel):
    email: str = Field(min_length=1, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                       description="Email адрес пользователя")
    password: str = Field(min_length=8, max_length=20, description="Пароль пользователя")


class UserLoginResponse(BaseModel):
    user: Dict[str, Any] = Field(min_length=1, description="Данные пользователя")
    accessToken: str = Field(min_length=1, description="Access токен")
    refreshToken: str = Field(min_length=1, description="Refresh токен")
    expiresIn: int = Field(gt=0, description="Время истечения токена в Unix timestamp")


# Модели для Movies API
class GetMoviesResponse(BaseModel):
    movies: List[Dict[str, Any]] = Field(min_length=1, description="Список фильмов")
    count: int = Field(gt=0, description="Общее количество фильмов")
    page: int = Field(gt=0, description="Текущая страница")
    pageSize: int = Field(gt=0, description="Размер страницы")
    pageCount: int = Field(gt=0, description="Общее количество страниц")


class CreateMovieRequest(BaseModel):
    name: str = Field(min_length=1, description="Название фильма")
    imageUrl: str = Field(min_length=1, description="URL постера фильма")
    price: int = Field(gt=0, description="Цена билета")
    description: str = Field(min_length=1, description="Описание фильма")
    location: str = Field(min_length=1, description="Локация показа")
    published: bool = Field(description="Опубликован ли фильм")
    genreId: int = Field(gt=0, description="ID жанра")

    @classmethod
    @field_validator("location")
    def validate_location(cls, value: str) -> str:
        if value not in ["SPB", "MSK"]:
            raise ValueError('location должен быть "MSK" или "SPB"')
        return value


class CreateMovieResponse(BaseModel):
    id: int = Field(gt=0, description="ID созданного фильма")
    name: str = Field(min_length=1, description="Название фильма")
    price: int = Field(gt=0, description="Цена билета")
    description: str = Field(min_length=1, description="Описание фильма")
    imageUrl: str = Field(min_length=1, description="URL постера фильма")
    location: str = Field(min_length=1, description="Локация показа")
    published: bool = Field(description="Опубликован ли фильм")
    genreId: int = Field(gt=0, description="ID жанра")
    genre: dict = Field(min_length=1, description="Данные жанра")
    createdAt: str = Field(min_length=1, description="Дата и время создания фильма в формате ISO 8601")
    rating: int = Field(ge=0, description="Рейтинг фильма")

    @classmethod
    @field_validator("location")
    def validate_location(cls, value: str) -> str:
        if value not in ["SPB", "MSK"]:
            raise ValueError('location должен быть "MSK" или "SPB"')
        return value

    @classmethod
    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value


class DeleteMovieResponse(CreateMovieResponse):
    reviews: list = Field(default_factory=list, description="Список отзывов")


class ParamsForGetMoviesRequest(BaseModel):
    pageSize: int = Field(default=None, gt=0, description="Размер страницы")
    page: int = Field(default=None, gt=0, description="Текущая страница")
    minPrice: int = Field(default=None, gt=0, description="Минимальная цена билета")
    maxPrice: int = Field(default=None, gt=0, description="Максимальная цена билета")
    locations: str = Field(default=None, min_length=1, description="Локация показа")
    published: bool = Field(default=None, description="Опубликован ли фильм")
    genreId: int = Field(default=None, gt=0, description="ID жанра")
    createdAt: str = Field(default=None, description="Дата и время создания фильма в формате ISO 8601")
