"""Модуль для роутов"""

__author__: str = "Старков Е.П."

from uuid import UUID

from docutils.nodes import description
from fastapi import APIRouter

from .services import AccessService

from . import schemas

auth_routes: APIRouter = APIRouter(prefix="/auth", tags=["auth"])


@auth_routes.post(
    "/login",
    description="Авторизация пользователя",
    response_model=schemas.LoginDataOut,
)
async def register_user(data: schemas.AccessValidateData):
    """Регистрация пользователя"""
    return await AccessService.login(data.login, data.password)


@auth_routes.post("/refresh-token", description="Обновление токена доступа", response_model=schemas.LoginDataOut)
async def refresh_token(token_data: schemas.RefreshTokenData) -> dict:
    """Обновление токена"""
    return await AccessService.refresh_token(token_data.refresh_token)
