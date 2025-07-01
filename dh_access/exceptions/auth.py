from dh_platform.exceptions import BaseAppException

from dh_access.consts import MIN_LOGIN_LEN, MAX_LOGIN_LEN

from fastapi import status


class NoLoginOrIncorrectLen(BaseAppException):
    _DETAIL = f"Пароль должен быть длинной от {MIN_LOGIN_LEN} до {MAX_LOGIN_LEN} символов"
    _CODE = status.HTTP_422_UNPROCESSABLE_ENTITY


class LoginAlreadyExists(BaseAppException):
    _DETAIL = "Данный логин уже используется"
    _CODE = status.HTTP_409_CONFLICT


class PasswordIncorrect(BaseAppException):
    _DETAIL = "Переданный пароль не верен"
    _CODE = status.HTTP_400_BAD_REQUEST


class LoginIncorrect(BaseAppException):
    _DETAIL = "Переданный логин не верен"
    _CODE = status.HTTP_400_BAD_REQUEST


class AccessDenied(BaseAppException):
    _DETAIL = "Пользователю запрещен доступ в систему"
    _CODE = status.HTTP_400_BAD_REQUEST

class MaxFailedAttempt(BaseAppException):
    _DETAIL = "Превышено количество попыток входа в систему. Восстановите пароль"
    _CODE = status.HTTP_400_BAD_REQUEST


class AccessBlocked(BaseAppException):
    _DETAIL = "Пользователю заблокирован доступ в систему"
    _CODE = status.HTTP_401_UNAUTHORIZED

__all__: list[str] = [
    "NoLoginOrIncorrectLen",
    "LoginAlreadyExists",
    "PasswordIncorrect",
    "LoginIncorrect",
    "MaxFailedAttempt",
    "AccessDenied",
    "AccessBlocked"
]