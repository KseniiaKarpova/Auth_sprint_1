from sqlalchemy.ext.asyncio import AsyncSession
from storages import AlchemyBaseStorage
from models.models import User
from fastapi import Depends
from db.postgres import create_async_session


class UserStorage(AlchemyBaseStorage):
    table = User
