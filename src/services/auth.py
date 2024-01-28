from functools import lru_cache

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from core.hasher import DataHasher
from exceptions import user_exists
from schemas.auth import UserLogin
from services import BaseService
from storages.user import UserStorage
from storages.user_history import UserHistoryStorage
from schemas.auth import UserCredentials, UserLogin
from exceptions import user_exists, user_created, unauthorized, incorrect_credentials
from core.hasher import DataHasher
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import create_async_session
from async_fastapi_jwt_auth import AuthJWT


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

    async def login(self, data: UserLogin, auth_jwt: AuthJWT):
        user = await self.storage.get(conditions={
            'login': data.login
        })
        if not user:
            raise incorrect_credentials
        is_valid = await DataHasher().verify(secret_word=data.password, hashed_word=user.password)
        if is_valid is False:
            raise unauthorized

        access_token = await auth_jwt.create_access_token(
            subject=user.login, fresh=True
        )
        refresh_token = await auth_jwt.create_refresh_token(subject=user.login)

        if self.observer:
            await self.observer.create(params={
                "user_id": user.uuid,
                "user_agent": data.agent,
                "refresh_token": refresh_token,
            })
        return {"access_token": access_token, "refresh_token": refresh_token}

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
