from datetime import datetime

from dh_platform.patterns.message_bus import message_bus
from dh_users.schemas.events import UserValidateEvent, UserAddEvent, UserDeleteEvent

from dh_access.consts import MIN_LOGIN_LEN, MAX_LOGIN_LEN
from dh_access.exceptions import NoLoginOrIncorrectLen, LoginAlreadyExists
from dh_access.helpers import hash_password
from dh_access.schemas import AccessInsertData
from dh_access.services import AccessService
from dh_access.models import AccessModel


async def _validate_auth_data(data: UserValidateEvent) -> None:
    login: str = data.login

    if not login or (MIN_LOGIN_LEN > len(login) < MAX_LOGIN_LEN):
        raise NoLoginOrIncorrectLen()

    if await AccessService.get_one_by_filter(login=login):
        raise LoginAlreadyExists()


async def _create_access_data(data: UserAddEvent) -> None:
    await AccessService.create(AccessInsertData(**{
        'login': data.login,
        'user_id': data.user_id,
        'hashed_password': hash_password(data.password),
        'role_id': data.role,
    }))


async def _delete_access_data(data: UserDeleteEvent) -> None:
    access_data: AccessModel | None = await AccessService.get_one_by_filter(user_id=data.user_id)

    if not access_data:
        return

    if data.force_delete:
        await AccessService.delete(access_data.id)
    else:
        access_data.date_deactivate = datetime.now()
        await AccessService.update(access_data)


def access_event_subscribe() -> None:
    message_bus.subscribe(UserValidateEvent, _validate_auth_data)
    message_bus.subscribe(UserAddEvent, _create_access_data)
    message_bus.subscribe(UserDeleteEvent, _delete_access_data)
