"""Модуль для сервиса доступа"""

__author__: str = "Старков Е.П."

from datetime import timedelta, datetime

from dh_platform.services import BaseService
from jose import jwt, JWTError

from dh_access.consts import MAX_LOGIN_TRY, TokenType
from dh_access.helpers import verify_password, create_token
from dh_access.models import AccessModel
from dh_access import exceptions as exc
from dh_access.schemas import AccessAttemptData
from dh_access.settings import access_settings


class AccessService(BaseService):
    """Сервис доступа"""

    _MODEL = AccessModel

    @classmethod
    async def login(cls, login: str, password: str) -> dict:
        access_data: AccessModel = await cls.get_one_by_filter(login=login)

        cls._check_access_data(access_data)

        if not verify_password(password, access_data.hashed_password):
            await cls.update(AccessAttemptData(
                id=access_data.id,
                failed_attempts=(access_data.failed_attempts or 0) + 1,
                last_login=access_data.last_login,
            ))
            raise exc.PasswordIncorrect()

        await cls.update(AccessAttemptData(id=access_data.id, failed_attempts=0, last_login=datetime.now()))

        return cls._create_token_data(access_data.user_id)

    @classmethod
    async def refresh_token(cls, token: str) -> dict:
        try:
            payload = jwt.decode(token, access_settings.SECRET_APP, algorithms=[access_settings.ALGORITHM])
            user_id: int = int(payload.get("sub"))

            if not user_id:
                raise exc.NoValidTokenException()

            # Проверяем, что токен является refresh токеном
            if payload.get("type") != TokenType.REFRESH:
                raise exc.NoValidTokenException()

            access_data: AccessModel = await AccessService.get_one_by_filter(user_id=user_id)

            if not access_data:
                raise exc.NoValidTokenException()

            if access_data.date_deactivate:
                raise exc.AccessBlocked()

            # Создаем новые токены
            return cls._create_token_data(user_id)
        except JWTError:
            raise exc.NoValidTokenException()

    @staticmethod
    def _check_access_data(access_data: AccessModel) -> None:
        if not access_data:
            raise exc.LoginIncorrect()

        if access_data.date_deactivate:
            raise exc.AccessDenied()

        if access_data.failed_attempts >= MAX_LOGIN_TRY:
            raise exc.MaxFailedAttempt()

    @staticmethod
    def _create_token_data(user_id: int) -> dict:
        access_token = create_token(
            {"sub": str(user_id)}, timedelta(minutes=access_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_token(
            {"sub": str(user_id)}, timedelta(days=access_settings.REFRESH_TOKEN_EXPIRE_DAYS), TokenType.REFRESH
        )

        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "refresh_token": refresh_token,
        }
