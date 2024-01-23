from sqlalchemy.ext.asyncio import AsyncSession
from storages import AlchemyBaseStorage
from models.models import User
from fastapi import Depends
from db.postgres import create_async_session


class UserStorage(AlchemyBaseStorage):
    table = User
    def __init__(self, session: AsyncSession = None) -> None:
        super().__init__(session)

def get_user_storage(session=Depends(create_async_session)):
    return UserStorage(session=session)