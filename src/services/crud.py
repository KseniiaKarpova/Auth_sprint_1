from functools import lru_cache
from fastapi import Depends
from services import AbstractCrudService
from storages.role import Roletorage, get_role_storage
from storages.user_role import UserRoleStorage, get_user_role_storage
from sqlalchemy.exc import IntegrityError
from exceptions import role_already_exist_error, server_error, role_not_found, crud_not_found


class CrudService(AbstractCrudService):
    def __init__(self, storage_user: UserRoleStorage, storage_role: Roletorage):
        self.storage_user = storage_user
        self.storage_role = storage_role

    async def create_role(self, name: str):
        ''' создание роли '''
        try:
            res = await self.storage_role.create(params={
                'name': name
            })
            return res
        except IntegrityError:
            raise role_already_exist_error
        except Exception:
            raise server_error

    async def delete_role(self, type: str, val):
        ''' удаление роли '''
        try:
            res = await self.storage_role.delete(conditions={
                type: val
            })
            return res['rowcount']
        except IntegrityError:
            raise role_already_exist_error
        except Exception:
            raise server_error

    async def set_role(self, old_data=dict, new_data=dict):
        ''' изменение роли '''
        try:
            res = await self.storage_role.update(old_data, new_data)
            return res['rowcount']
        except IntegrityError:
            raise role_not_found
        except Exception:
            raise server_error

    async def show_all_role(self):
        ''' просмотр всех ролей '''
        try:
            res = await self.storage_role.get_many({})
            return res
        except IntegrityError:
            raise role_not_found
        except Exception:
            raise server_error

    async def add_role(self, user_id: str, role_id: str):
        ''' назначить пользователю роль '''
        try:
            res = await self.storage_user.create(params={
                'user_id': user_id,
                'role_id': role_id
            })
            return res
        except IntegrityError:
            raise crud_not_found
        except Exception:
            raise server_error

    async def deprive_role(self, user_id: str, role_id: str):
        ''' отобрать у пользователя роль '''
        try:
            res = await self.storage_user.delete(conditions={
                'user_id': user_id,
                'role_id': role_id
            })
            return res['rowcount']
        except IntegrityError:
            raise role_already_exist_error
        except Exception:
            raise server_error

    async def check_role(self, user_id, role_id):
        ''' проверка наличия прав у пользователя '''
        try:
            res = await self.storage_user.exists(conditions={
                'user_id': user_id,
                'role_id': role_id
            })
            return res
        except IntegrityError:
            raise role_not_found
        except Exception:
            raise server_error


@lru_cache()
def get_crud_service(
    role_storage: Roletorage = Depends(get_role_storage),
    user_storage: UserRoleStorage = Depends(get_user_role_storage)
) -> CrudService:
    return CrudService(storage_user=user_storage, storage_role=role_storage)
