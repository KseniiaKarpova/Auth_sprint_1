"""
    CRUD для управления ролями:

        - создание роли,
        - удаление роли,
        - изменение роли,
        - просмотр всех ролей.
        - назначить пользователю роль
        - отобрать у пользователя роль
        - метод для проверки наличия прав у пользователя
"""
from abc import ABC, abstractmethod


class AbstractCrudStorage(ABC):
    @abstractmethod
    async def get(self, id: str):
        pass

    @abstractmethod
    async def update(self, id: str, data):
        pass

    @abstractmethod
    async def delete(self, id: str):
        pass

    @abstractmethod
    async def create(self, id: str, data):
        pass


class AbstractCrudManagement(ABC):
    @abstractmethod
    async def create_role(self, id: str, data):
        ''' создание роли '''
        pass

    @abstractmethod
    async def delete_role(self, id: str):
        ''' удаление роли '''
        pass

    @abstractmethod
    async def set_role(self, id, data):
        ''' изменение роли '''
        pass

    @abstractmethod
    async def show_all_role(self):
        ''' просмотр всех ролей '''
        pass

    @abstractmethod
    async def add_role(self, id: str, data, user):
        ''' назначить пользователю роль '''
        pass

    @abstractmethod
    async def deprive_role(self, id: str, user):
        ''' отобрать у пользователя роль '''
        pass

    @abstractmethod
    async def check_role(self, id: str, user):
        ''' проверка наличия прав у пользователя '''
        pass
