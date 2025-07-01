"""Модуль для модели ролей"""

__author__: str = "Старков Е.П."

from dh_platform.models import BaseModel, IDMixin, TimestampMixin
from dh_users.models import UserModel
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Role(BaseModel, IDMixin, TimestampMixin):
    """
    Модель ролей

    Warnings:
        Поле permissions хранит в себе словарь, вида область: уровень доступа
    """

    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255))
    permissions: Mapped[dict[str, int]] = mapped_column(JSONB)
