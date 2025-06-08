"""Модуль для модели ролей"""

__author__: str = "Старков Е.П."

from dh_platform.models import BaseModel, IDMixin, TimestampMixin
from dh_users.models import UserModel
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

user_role_association: Table = Table(
    "user_role_association",
    BaseModel.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("role_id", ForeignKey("role.id")),
)


class Role(BaseModel, IDMixin, TimestampMixin):
    """
    Модель ролей

    Warnings:
        Поле permissions хранит в себе словарь, вида область: уровень доступа
    """

    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255))
    permissions: Mapped[dict[str, int]] = mapped_column(JSONB)

    users: Mapped[list] = relationship(UserModel, secondary=user_role_association)
