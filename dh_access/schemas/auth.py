"""Модуль для схем данных аутентификации"""

__author__: str = "Старков Е.П."

from datetime import datetime

from pydantic import BaseModel


class AccessPublicData(BaseModel):
    """
    Публичные данные доступа

    Attributes:
        login (str): Логин пользователя
    """

    login: str


class AccessValidateData(AccessPublicData):
    """
    Данные для валидации

    Attributes:
        password (str): Пароль пользователя
    """

    password: str


class AccessAddData(AccessValidateData):
    """
    Данные для валидации

    Attributes:
        role (int | None): Идентификатор роли
        user_id (int): Идентификатор пользователя
    """

    role: int | None
    user_id: int


class AccessInsertData(AccessPublicData):
    hashed_password: str
    user_id: int


class RefreshTokenData(BaseModel):
    refresh_token: str


class LoginDataOut(RefreshTokenData):
    access_token: str
    token_type: str


class AccessAttemptData(BaseModel):
    id: int
    failed_attempts: int | None
    last_login: datetime | None


__all__: list[str] = [
    "AccessPublicData", "AccessValidateData", "AccessAddData", "AccessInsertData", "LoginDataOut",
    "AccessAttemptData", "RefreshTokenData"
]
