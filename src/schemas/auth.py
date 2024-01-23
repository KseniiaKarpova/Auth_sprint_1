from datetime import timedelta
from fastapi import Form
from pydantic import BaseModel, Field

from core.config import settings


class UserCredentials(BaseModel):
    login: str = Form(...)
    password: str = Form(...)
    email: str = Form(...)


class UserLogin(BaseModel):
    login: str = Form(...)
    password: str = Form(...)
    agent: str = Form(...)


class AuthSettingsSchema(BaseModel):
    authjwt_secret_key: str = settings.auth.secret_key
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    authjwt_algorithm: str = "HS256"
    access_expires: int = timedelta(minutes=15)
    refresh_expires: int = timedelta(days=30)


class LoginResponseSchema(BaseModel):
    access_token: str = Field(description='Access token value')
    refresh_token: str = Field(description='Refresh token value')
