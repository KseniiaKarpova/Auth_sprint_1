from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import create_async_session
from models.models import User
from storages import AlchemyBaseStorage


class UserStorage(AlchemyBaseStorage):
    table = User

    def __init__(self, session: AsyncSession = None) -> None:
        super().__init__(session)


def get_user_storage(session=Depends(create_async_session)):
    return UserStorage(session=session)
