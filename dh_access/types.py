"""Модуль для типов данных"""

__author__: str = "Старков Е.П."

from typing import TypeAlias

RolesData: TypeAlias = dict[str, dict[str, dict[str, int | str]]]
