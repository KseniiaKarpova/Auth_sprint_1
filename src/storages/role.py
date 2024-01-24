from sqlalchemy.ext.asyncio import AsyncSession
from storages import AlchemyBaseStorage
from models.models import Role
from fastapi import Depends
from db.postgres import create_async_session


class Roletorage(AlchemyBaseStorage):
    table = Role

    def __init__(self, session: AsyncSession = None) -> None:
        super().__init__(session)


def get_role_storage(session=Depends(create_async_session)):
    return Roletorage(session=session)
