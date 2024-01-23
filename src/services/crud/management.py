from services.crud import AbstractCrudManagement
from services.crud import AbstractCrudStorage
from models.models import Role, UserRole


class CrudManagement(AbstractCrudManagement):

    def __init__(self, db: AbstractCrudStorage):
        self.db = db

    async def create_role(self, name: str):
        ''' создание роли '''
        role = Role(name=name)
        print(self.db.create(role))

    async def delete_role(self, id: str):
        ''' удаление роли '''
        print(self.db.delete(id))

    async def set_role(self, id, data):
        ''' изменение роли '''
        pass

    async def show_all_role(self):
        ''' просмотр всех ролей '''
        pass

    async def add_role(self, id: str, data, user):
        ''' назначить пользователю роль '''
        pass

    async def deprive_role(self, id: str, user):
        ''' отобрать у пользователя роль '''
        pass

    async def check_role(self, id: str, user):
        ''' проверка наличия прав у пользователя '''
        pass