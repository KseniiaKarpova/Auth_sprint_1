from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import create_async_session
from models.models import User
from storages import AlchemyBaseStorage


class UserStorage(AlchemyBaseStorage):
    table = User
