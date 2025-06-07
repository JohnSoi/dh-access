"""Модуль для модели доступа"""

__author__: str = "Старков Е.П."

from datetime import datetime

from dh_platform.models import BaseModel, IDMixin, TimestampMixin
from sqlalchemy import Column, ForeignKey, String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dh_access.consts import PermissionAccessLevel, GUEST_ROLE_NAME


class Access(BaseModel, IDMixin, TimestampMixin):
    login: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_attempts: Mapped[int] = mapped_column(Integer, default=0)
    date_deactivate: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Связи
    user_id = Column(Integer, ForeignKey("user.id"))
    role_id = Column(Integer, ForeignKey("role.id"))

    # Relationships
    user = relationship("User")
    role = relationship("Role")

    @property
    def access_level(self) -> str:
        """Вычисляемый уровень доступа"""
        if not self.role:
            return GUEST_ROLE_NAME

        return self.role.name.lower()

    @property
    def is_active(self) -> bool:
        """Пользователь активен"""
        return not bool(self.date_deactivate)

    def has_access(self, area: str, need_level: PermissionAccessLevel) -> bool:
        """
        Проверка доступа

        Args:
            area (str): область проверки прав
            need_level (PermissionAccessLevel): необходимый уровень доступа

        Returns:
            (bool): есть доступ к области необходимого уровня
        """
        if area not in self.role.permissions:
            return False

        return self.role.permissions[area] <= need_level