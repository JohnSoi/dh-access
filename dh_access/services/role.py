"""Модуль для сервиса ролей"""

__author__: str = "Старков Е.П."

from dh_platform.services import BaseService

from dh_access.models import RoleModel


class RoleService(BaseService):
    """Сервис ролей"""

    _MODEL = RoleModel
