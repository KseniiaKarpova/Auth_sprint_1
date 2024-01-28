import json
from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, Body
from schemas.auth import JWTUserData, LoginResponseSchema, UserLogin
from uuid import UUID
from exceptions import incorrect_credentials, unauthorized
from core.hasher import DataHasher
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import create_async_session
from storages.user import UserStorage
from models.models import User


class JWTCoverter:
    async def get_data(self, payload: dict):
        return json.loads(payload)
    
    async def convert_data(self, payload: dict):
        return json.dumps(payload)


async def get_current_user(Authorize: AuthJWT = Depends(),
                           jwt_converter: JWTCoverter = Depends(JWTCoverter)) -> JWTUserData:
    """
    Dependency to get the current user from the JWT token.
    """
    await Authorize.jwt_required()
    jwt_subject = await Authorize.get_jwt_subject()
    subject = await jwt_converter.get_data(payload=jwt_subject)
    return JWTUserData(
        login=subject['login'],
        uuid=UUID(subject['uuid']),
    )


async def check_user(
        user_credentials: UserLogin = Body(),
        session: AsyncSession = Depends(create_async_session)) -> User:
    storage = UserStorage(session=session)
    user = await storage.get(conditions={
            'login': user_credentials.login
        })

    if not user:
        raise incorrect_credentials
    is_valid = await DataHasher().verify(secret_word=user_credentials.password, hashed_word=user.password)

    if is_valid is False:
        raise unauthorized
    return user


async def user_tokens(
        auth_jwt: AuthJWT = Depends(),
        jwt_converter: JWTCoverter = Depends(JWTCoverter),
        user: User = Depends(check_user),
        ) -> LoginResponseSchema:
    subject = await jwt_converter.convert_data({
        'login': user.login,
        'uuid': str(user.uuid)
    })
    access_token = await auth_jwt.create_access_token(
        subject=subject, fresh=True
    )
    refresh_token = await auth_jwt.create_refresh_token(subject=subject)

    return LoginResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )
