# pylint: disable=broad-exception-caught, missing-kwoa
"""Модуль для инициализатора ролей"""

__author__: str = "Старков Е.П."

import logging

from dh_access.schemas import RoleData
from dh_access.services import RoleService
from dh_access.types import RolesData

logger = logging.getLogger("dh_logger")


async def role_init(roles_data: RolesData) -> None:
    """
    Инициализатор ролей

    Args:
        roles_data: список ролей системы

    Examples:
        >>> from dh_access.initializers import role_init
        >>> from dh_access.consts import PermissionAccessLevel
        >>>
        >>> ROLES_DATA: RolesData = {
        ...     "ADMIN": {
        ...         "permissions": {"users": PermissionAccessLevel.DELETE},
        ...         "description": "Роль с полным доступом в систему. "
        ...         "Может просматривать все сущности и производить все операции над ними",
        ...     },
        ... }
        >>>
        >>> @asynccontextmanager
        >>> async def lifespan(_: FastAPI):
        ...     await role_init(ROLES_DATA)
    """
    try:
        logger.info("Старт инициализации ролей")
        added_roles_data = await RoleService.list()
        no_added_roles: list[str] = list(set(roles_data) - set(role.name for role in added_roles_data))
        logger.info("Список ролей для добавления: %s", ", ".join(no_added_roles))

        for role in no_added_roles:
            await RoleService.create(
                RoleData(**{
                    "name": role,
                    "permissions": roles_data[role]["permissions"],
                    "description": roles_data[role]["description"],
                })
            )
    except Exception as e:
        logger.info("Ошибка при добавлении роли: %s", e)
        print(e)
