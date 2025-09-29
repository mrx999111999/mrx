from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enums.roles import Roles
import datetime
import re


class UserRegisterRequest(BaseModel):
    email: str = Field(min_length=1, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                       description="Email адрес пользователя")
    fullName: str = Field(min_length=1, description="Полное имя пользователя")
    password: str = Field(min_length=8, max_length=20, description="Пароль пользователя")
    passwordRepeat: str = Field(min_length=8, max_length=20, description="Повтор пароля для подтверждения")
    roles: list[Roles] = Field(min_length=1, description="Роли пользователя")
    banned: Optional[bool] = None
    verified: Optional[bool] = None

    @classmethod
    @field_validator("password")
    def validate_password_strength(cls, value: str) -> str:
        """Валидация сложности пароля по требованиям"""
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

    # Добавляем кастомный JSON-сериализатор для Enum
    class Config:
        json_encoders = {
            Roles: lambda v: v.value  # Преобразуем Enum в строку
        }


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
