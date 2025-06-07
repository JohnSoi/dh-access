
from dh_access.services import RoleService
from dh_access.types import RolesData


async def role_init(roles_data: RolesData):
    try:
        added_roles_data = await RoleService.list()
        no_added_roles: list[str] = list(set(roles_data) - set(role.name for role in added_roles_data))

        for role in no_added_roles:
            await RoleService.create({
                "name": role,
                "permissions": roles_data[role]["permissions"],
                "description": roles_data[role]["description"],
            })
    except Exception as e:
        print(e)
