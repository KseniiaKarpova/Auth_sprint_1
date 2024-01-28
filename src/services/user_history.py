from functools import lru_cache

from fastapi import Depends
from services import BaseService
from storages.user_history import UserHistoryStorage
from models.models import UserHistory
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import create_async_session
from uuid import UUID


class UserHistoryService(BaseService):
    def __init__(self, storage: UserHistoryStorage):
        self.storage = storage

    async def user_login_history(self, user_id: UUID) -> list[UserHistory]:
        return await self.storage.get_many(
            conditions={
                'user_id': user_id,
            }
        )


@lru_cache()
def get_user_history_service(
    session: AsyncSession = Depends(create_async_session)
) -> UserHistoryService:
    return UserHistoryService(
        storage=UserHistoryStorage(session=session))
