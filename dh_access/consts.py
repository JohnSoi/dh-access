"""Константы модуля"""

__author__: str = "Старков Е.П."

from enum import IntEnum


class PermissionAccessLevel(IntEnum):
    """
    Константы уровня доступа

    Attributes:
        DENIED (int): Доступ запрещен
        READ (int): Доступ на чтение
        WRITE (int): Доступ на запись
        DELETE (int): Доступ на удалить
    """

    DENIED = 0
    READ = 1
    WRITE = 2
    DELETE = 3


GUEST_ROLE_NAME: str = "guest"

MIN_LOGIN_LEN: int = 4
MAX_LOGIN_LEN: int = 50
