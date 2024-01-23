from services.crud import AbstractCrudStorage
from db.postgres import create_async_session
from models.models import Role, UserRole
from exceptions import role_already_exist_error, role_not_found
from sqlalchemy import select


class PostgresCrudStorage(AbstractCrudStorage):

    async def get(self, id: str):
        try:
            session = await create_async_session()
            async with session.begin():
                result = await session.execute(select(Role).
                                           where(Role.uuid == id).
                                           limit(1))
            for i in result:
                return i
        except Exception:
            raise role_not_found

    async def update(self, object):
        pass

    async def delete(self, id):
        try:
            session = await create_async_session()
            async with session.begin():
                row = await session.execute(select(Role).where(Role.uuid == id))
                row = row.scalar_one()
                await session.delete(row)
                await session.commit()
        except Exception:
            raise role_not_found

    async def create(self, object):
        try:
            session = await create_async_session()
            async with session.begin():
                session.add(object)
        except Exception:
            raise role_already_exist_error
