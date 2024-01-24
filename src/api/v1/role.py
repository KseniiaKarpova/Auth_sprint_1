from services.crud import CrudService, get_crud_service
from fastapi import APIRouter, Depends, status
from exceptions import role_already_exist_error, role_not_found, crud_not_found


router = APIRouter()


@router.patch(
    "/",
    response_description="Create role",
    summary="",
    status_code=status.HTTP_201_CREATED,
)
async def create_role(
        service: CrudService = Depends(get_crud_service),
        name: str | None = None,
):
    result = await service.create_role(name)
    if result is None:
        raise role_already_exist_error
    return result


@router.delete(
    "/",
    response_description="Удаление роли",
    summary="",
    status_code=status.HTTP_200_OK
)
async def delete_role(
        service: CrudService = Depends(get_crud_service),
        type: str | None = None,
        value: str | None = None,
):
    result = await service.delete_role(type, value)
    if not result:
        raise role_not_found
    else:
        return 'Changes have been applied'


@router.post(
    "/",
    response_description="",
    summary="",
    description="Изменение роли",
    status_code=status.HTTP_200_OK
)
async def set_role(
        service: CrudService = Depends(get_crud_service),
        old: dict | None = None,
        new: dict | None = None,
):
    result = await service.set_role(old, new)
    if not result:
        raise role_not_found
    else:
        return 'Changes have been applied'


@router.get(
    "/",
    response_description="Просмотр всех ролей",
    summary="",
)
async def show_role(
        service: CrudService = Depends(get_crud_service),
):
    result = await service.show_all_role()
    if result is None:
        raise role_not_found
    return result

@router.patch(
    "/user/",
    response_description="Назначить пользователю роль",
    summary="",
)
async def add_role(
    service: CrudService = Depends(get_crud_service),
    user_id: str | None = None,
    role_id: str | None = None,
):
    result = await service.add_role(user_id, role_id)
    if result is None:
        raise crud_not_found
    return result


@router.delete(
    "/user/",
    response_description="Oтобрать у пользователя роль",
    summary="",
    status_code=status.HTTP_200_OK
)
async def deprive_role(
    service: CrudService = Depends(get_crud_service),
    user_id: str | None = None,
    role_id: str | None = None,
):
    result = await service.deprive_role(user_id, role_id)
    if not result:
        raise crud_not_found
    else:
        return 'Changes have been applied'


@router.get(
    "/user/",
    response_description="Проверка наличия прав у пользователя",
    summary="",
)
async def check_role(
    service: CrudService = Depends(get_crud_service),
    user_id: str | None = None,
    role_id: str | None = None,
):
    result = await service.check_role(user_id, role_id)
    return result
