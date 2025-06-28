from dh_platform.patterns.message_bus import message_bus
from dh_users.schemas.events import UserValidateEvent, UserAddEvent

from dh_access.consts import MIN_LOGIN_LEN, MAX_LOGIN_LEN
from dh_access.exceptions.auth import NoLoginOrIncorrectLen, LoginAlreadyExists
from dh_access.helpers import hash_password
from dh_access.schemas.auth import AccessInsertData
from dh_access.services import AccessService


async def _validate_auth_data(data: UserValidateEvent) -> None:
    import pydevd_pycharm
    pydevd_pycharm.settrace('localhost', port=8888, stdoutToServer=True, stderrToServer=True)
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
    }))


def access_event_subscribe() -> None:
    message_bus.subscribe(UserValidateEvent, _validate_auth_data)
    message_bus.subscribe(UserAddEvent, _create_access_data)

