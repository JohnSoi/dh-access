from pydantic import BaseModel


class RoleData(BaseModel):
    """
    Данные о роли

    Attributes:
        name (str): Название роли
        permissions (dict): Разрешения по областям
        description (str): Описания
    """
    name: str
    permissions: dict
    description: str
