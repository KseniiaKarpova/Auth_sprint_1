from fastapi import APIRouter, Depends
from schemas.auth import JWTUserData
from services.user_history import get_user_history_service, UserHistoryService
from core.handlers import get_current_user
from schemas.user_history import UserHistory


router = APIRouter()

@router.get("", response_model=list[UserHistory])
async def login_history(
        current_user: JWTUserData = Depends(get_current_user),
        service : UserHistoryService = Depends(get_user_history_service)):
    return await service.user_login_history(user_id=current_user.uuid)
