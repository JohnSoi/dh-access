from dh_platform.exceptions import BaseAppException

from dh_access.consts import MIN_LOGIN_LEN, MAX_LOGIN_LEN

from fastapi import status


class NoLoginOrIncorrectLen(BaseAppException):
    _DETAIL = f"Пароль должен быть длинной от {MIN_LOGIN_LEN} до {MAX_LOGIN_LEN} символов"
    _CODE = status.HTTP_422_UNPROCESSABLE_ENTITY


class LoginAlreadyExists(BaseAppException):
    _DETAIL = "Данный логин уже используется"
    _CODE = status.HTTP_409_CONFLICT
