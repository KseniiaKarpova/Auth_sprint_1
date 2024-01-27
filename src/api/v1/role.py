from fastapi import APIRouter, Depends, Query, status
from async_fastapi_jwt_auth import AuthJWT
from exceptions import crud_not_found, role_already_exist_error, role_not_found, forbidden_error
from models.models import Role
from services.crud import CrudService, get_crud_service
from services.auth import AuthService, get_auth_service


router = APIRouter()


@router.patch(
    "/",
    response_description="Create role",
    summary="",
    status_code=status.HTTP_201_CREATED,
)
async def create_role(
    Authorize: AuthJWT = Depends(),
    auth: AuthService = Depends(get_auth_service),
    service: CrudService = Depends(get_crud_service),
    name: str | None = None,
):
    await Authorize.jwt_required()
    current_user = await Authorize.get_jwt_subject()
    isSuper = await auth.is_super_user(current_user)
    if not isSuper:
        raise forbidden_error

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
    Authorize: AuthJWT = Depends(),
    auth: AuthService = Depends(get_auth_service),
    service: CrudService = Depends(get_crud_service),
    type: str = Query(Role.get_colums()[0], enum=Role.get_colums()),
    value: str | None = None,
):
    await Authorize.jwt_required()
    current_user = await Authorize.get_jwt_subject()
    isSuper = await auth.is_super_user(current_user)
    if not isSuper:
        raise forbidden_error

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
    Authorize: AuthJWT = Depends(),
    auth: AuthService = Depends(get_auth_service),
    service: CrudService = Depends(get_crud_service),
    old: dict | None = None,
    new: dict | None = None,
):
    await Authorize.jwt_required()
    current_user = await Authorize.get_jwt_subject()
    isSuper = await auth.is_super_user(current_user)
    if not isSuper:
        raise forbidden_error

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
    Authorize: AuthJWT = Depends(),
    auth: AuthService = Depends(get_auth_service),
    service: CrudService = Depends(get_crud_service),
):
    await Authorize.jwt_required()
    current_user = await Authorize.get_jwt_subject()
    isSuper = await auth.is_super_user(current_user)
    if not isSuper:
        raise forbidden_error

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
    Authorize: AuthJWT = Depends(),
    auth: AuthService = Depends(get_auth_service),
    service: CrudService = Depends(get_crud_service),
    user_id: str | None = None,
    role_id: str | None = None,
):
    await Authorize.jwt_required()
    current_user = await Authorize.get_jwt_subject()
    isSuper = await auth.is_super_user(current_user)
    if not isSuper:
        raise forbidden_error

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
    Authorize: AuthJWT = Depends(),
    auth: AuthService = Depends(get_auth_service),
    service: CrudService = Depends(get_crud_service),
    user_id: str | None = None,
    role_id: str | None = None,
):
    await Authorize.jwt_required()
    current_user = await Authorize.get_jwt_subject()
    isSuper = await auth.is_super_user(current_user)
    if not isSuper:
        raise forbidden_error

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
    Authorize: AuthJWT = Depends(),
    auth: AuthService = Depends(get_auth_service),
    service: CrudService = Depends(get_crud_service),
    user_id: str | None = None,
    role_id: str | None = None,
):
    await Authorize.jwt_required()
    current_user = await Authorize.get_jwt_subject()
    isSuper = await auth.is_super_user(current_user)
    if not isSuper:
        raise forbidden_error

    result = await service.check_role(user_id, role_id)
    return result
