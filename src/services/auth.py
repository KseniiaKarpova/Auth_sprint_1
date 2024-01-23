from functools import lru_cache
from fastapi import Depends
from services import BaseService
from storages.user import UserStorage, get_user_storage
from schemas.auth import UserCredentials
from exceptions import user_exists, user_created, unauthorized, incorrect_credentials
from core.hasher import DataHasher
from sqlalchemy.exc import IntegrityError


class AuthService(BaseService):
    def __init__(self, storage: UserStorage):
        self.storage = storage
    
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

    async def login(self, data: UserCredentials):
        user = await self.storage.get(conditions={
            'login': data.login
        })
        if not user:
            raise incorrect_credentials
        is_valid = await DataHasher().verify(secret_word=data.password, hashed_word=user.password)
        if is_valid is True:
            return user
        raise unauthorized


@lru_cache()
def get_auth_service(
    storage: UserStorage = Depends(get_user_storage),
) -> AuthService:
    return AuthService(storage=storage)
