from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, Header
from redis.asyncio import Redis

from db.redis import get_redis
from exceptions import unauthorized
from schemas.auth import AuthSettingsSchema, LoginResponseSchema, UserLogin

router = APIRouter()


@AuthJWT.load_config
def get_auth_config():
    return AuthSettingsSchema()


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    redis = get_redis()
    entry = await redis.get(jti)
    return entry and entry == "true"


@router.post("/login", response_model=LoginResponseSchema)
async def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    if user.login != "test" or user.password != "test":
        raise unauthorized

    access_token = await Authorize.create_access_token(
        subject=user.login, fresh=True
    )
    refresh_token = await Authorize.create_refresh_token(subject=user.login)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
async def refresh(Authorize: AuthJWT = Depends()):
    await Authorize.jwt_refresh_token_required()

    current_user = await Authorize.get_jwt_subject()
    new_access_token = await Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.post("/logout")
async def logout(
        redis: Redis = Depends(get_redis),
        refresh_token: str = Header(..., alias="X-Access-Token"),
        access_token: str = Header(..., alias="X-Refresh-Token")):
    if access_token:
        await redis.setex(access_token, AuthSettingsSchema().access_expires, "true")
    if refresh_token:
        await redis.setex(refresh_token, AuthSettingsSchema().refresh_expires, "true")
    return {"detail": "User successfully logged out"}
