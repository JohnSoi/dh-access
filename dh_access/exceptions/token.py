from dh_platform.exceptions import BaseAppException
from fastapi import status


class NoValidTokenException(BaseAppException):
    _DETAIL = "Данные токена не валидны"
    _CODE = status.HTTP_401_UNAUTHORIZED

