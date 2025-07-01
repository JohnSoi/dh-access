from dh_platform.exceptions import BaseAppException


class NoUserIdentifierException(BaseAppException):
    _DETAIL = "Не передан ни один идентификатор пользователя для обогащения"
