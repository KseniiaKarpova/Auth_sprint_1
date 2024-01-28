from functools import lru_cache
import json
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from core.hasher import DataHasher
from exceptions import user_exists
from services import BaseService
from storages.user import UserStorage
from storages.user_history import UserHistoryStorage
from schemas.auth import UserCredentials
from exceptions import user_exists, user_created
from core.hasher import DataHasher
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import create_async_session


class AuthService(BaseService):
    def __init__(self, storage: UserStorage, observer: UserHistoryStorage):
        self.storage = storage
        self.observer = observer

    async def registrate(self, data: UserCredentials):
        try:
            hashed_password = await DataHasher().generate_word_hash(secret_word=data.password)
            await self.storage.create(params={
                'password': hashed_password,
                'login': data.login,
                'email': data.email,
            })
            return user_created
        except IntegrityError:
            raise user_exists

    async def is_super_user(self, login):
        status = await self.storage.exists(conditions={
            'login': login,
            'is_superuser': True
        })
        return status


@lru_cache()
def get_auth_service(
    session: AsyncSession = Depends(create_async_session)
) -> AuthService:
    return AuthService(
        storage=UserStorage(session=session),
        observer=UserHistoryStorage(session=session))
