from functools import lru_cache
from fastapi import Depends
from services.crud import AbstractCrudManagement, AbstractCrudStorage
from services.crud.management import CrudManagement
from services.crud.postgres_storage import PostgresCrudStorage


class RoleService:
    def __init__(self, management: AbstractCrudManagement):
        self.management = management

    async def create(self, name: str):
        data = await self.management.create_role(name)
        return data

    async def delete(self, id):
        data = await self.management.delete_role(id)
        return data


@lru_cache()
def get_role_service(
    storage: AbstractCrudManagement = Depends(PostgresCrudStorage),
) -> RoleService:
    manager = CrudManagement(storage)
    return RoleService(manager)
