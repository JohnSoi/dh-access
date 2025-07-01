"""Модуль базовых настроек"""

__author__: str = "Старков Е.П."

from functools import lru_cache

from pydantic_settings import BaseSettings


class AccessSettings(BaseSettings):
    """
    Настройки доступа

    Attributes:
        SECRET_APP (str): Секрет приложения
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Срок жизни токена доступа
        REFRESH_TOKEN_EXPIRE_DAYS (int): Срок жизни токена обновления
        ALGORITHM (str): Алгоритм шифрования токена
    Warnings:
        Данные переменные должны быть описаны в файле .env
    """

    SECRET_APP: str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    REFRESH_TOKEN_EXPIRE_DAYS : int
    ALGORITHM: str

    class Config:
        """Класс конфигурации настроек"""

        env_prefix = "AUTH_"
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_access_settings() -> AccessSettings:
    """
    Получение объекта базовых настроек

    Returns:
        BaseAppSettings: Экземпляр класса базовых настроек
    Examples:
        Пример использования в конфиге приложений:

        >>> from pydantic import Field
        >>> from pydantic_settings import BaseSettings
        >>> from dh_platform.settings import get_core_settings, BaseAppSettings
        >>> from dh_access.settings import get_access_settings, AccessSettings
        >>>
        >>> class AllSettings(BaseSettings):
        ...     core: BaseAppSettings = Field(default_factory=get_core_settings)
        ...     access: AccessSettings = Field(default_factory=get_access_settings)
        ...
        ...     class Config:
        ...         env_nested_delimiter = "__"
        >>>
        >>> @lru_cache
        >>> def get_all_settings() -> AllSettings:
        ...    return AllSettings()
    """
    return AccessSettings() # type: ignore[call-arg]


access_settings: AccessSettings = get_access_settings()


__all__: list[str] = ["get_access_settings", "AccessSettings", "access_settings"]
