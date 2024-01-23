from services.role import RoleService, get_role_service
from fastapi import APIRouter, Depends
from exceptions import role_already_exist_error, role_not_found


router = APIRouter()


@router.patch(
    "/",
    response_description="Create role",
    summary="",
    description="",
)
async def create(
        service: RoleService = Depends(get_role_service),
        name: str | None = None,
):
    file = await service.create(name)
    if not file:
        raise role_already_exist_error
    return file

