from typing import TypeVar
from uuid import UUID

from dh_users.services import UserService
from dh_users.models import UserModel
from pydantic import BaseModel
from dh_platform.models import BaseModel as BaseAppModel

from .consts import DEFAULT_RENDER_CONFIG
from .exceptions import NoUserIdentifierException
from ..services import AccessService, RoleService
from ..models import AccessModel, RoleModel

PydanticModel = TypeVar("PydanticModel", bound=BaseModel)
AppModel = TypeVar("AppModel", bound=BaseAppModel)


async def add_access_info(model: PydanticModel, config: dict | None) -> None:
    render_config: dict = DEFAULT_RENDER_CONFIG.copy()
    render_config.update(config or {})

    user_id: int = await _get_user_id(model, config)
    access_data: AccessModel = await AccessService.get_one_by_filter(user_id=user_id)

    _set_fields(render_config.get("Fields", []), model, access_data)
    await _add_role_data(model, render_config, access_data.role_id)


async def _get_user_id(model: PydanticModel, config: dict | None) -> int:
    user_id: int | None = getattr(model, config.get("UserIdFieldName"))
    user_uuid: UUID | None = getattr(model, config.get("UserUuidFieldName"))

    if not user_id and not user_uuid:
        raise NoUserIdentifierException()

    if not user_id:
        user_data: UserModel = await UserService.get_one_by_filter(uuid=user_uuid)
        user_id = user_data.id

    return user_id


async def _add_role_data(model: PydanticModel, config: dict | None, role_id: int) -> None:
    if not config.get("AddRole"):
        return

    role_data: RoleModel = await RoleService.get_one_by_filter(id=role_id)

    _set_fields(config.get("RoleFields", []), model, role_data)


def _set_fields(fields: list[str], model: PydanticModel, data: AppModel) -> None:
    for field in fields:
        setattr(model, field, getattr(data, field))
