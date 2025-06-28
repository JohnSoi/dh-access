"""Модуль для сервиса доступа"""

__author__: str = "Старков Е.П."

from dh_platform.services import BaseService

from dh_access.models import AccessModel


class AccessService(BaseService):
    """Сервис доступа"""

    _MODEL = AccessModel
