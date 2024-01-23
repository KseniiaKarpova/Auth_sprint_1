from functools import lru_cache
from fastapi import Depends
from services import BaseService
from storages.user import UserStorage, get_user_storage
from schemas.auth import UserLogin
from exceptions import user_exists
from core.hasher import DataHasher
from sqlalchemy.exc import IntegrityError


class AuthService(BaseService):
    def __init__(self, storage: UserStorage):
        self.storage = storage
    
    async def registrate(self, data: UserLogin):
        try:
            hashed_password = DataHasher().generate_word_hash(secret_word=data.password)
            await self.storage.create(params={
                'password': hashed_password,
                'login': data.login
            })
        except IntegrityError:
            raise user_exists
        
    async def verify(self, data: UserLogin):
        user = await self.storage.get(conditions={
            'login': data.login
        })        
        return DataHasher().verify(secret_word=UserLogin.password, hashed_word=user.password)


@lru_cache()
def get_auth_service(
    storage: UserStorage = Depends(get_user_storage),
) -> AuthService:
    return AuthService(storage=storage)
