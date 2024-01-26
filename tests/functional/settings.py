from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class PostgresDbSettings(BaseSettings):
    host: str = ...
    user: str = ...
    port: int = ...
    db: str = ...
    password: str = ...

    model_config = SettingsConfigDict(env_prefix='postgres_')


class RedisSettings(BaseSettings):
    host: str = ...
    port: int = ...

    model_config = SettingsConfigDict(env_prefix='redis_')


class AuthSettings(BaseSettings):
    secret_key: str = ...
    jwt_algorithm: str = ...
    model_config = SettingsConfigDict(env_prefix='auth_')


class HasherSettings(BaseSettings):
    algorithm: str = ...
    rounds: int = ...
    model_config = SettingsConfigDict(env_prefix='hasher_')


class TestSettings(BaseSettings):
    project_name: str = 'Pytest auth api'

    db: PostgresDbSettings = PostgresDbSettings()
    db_dsn: str = f'postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.db}'

    api_url: str = f''
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()
    hasher: HasherSettings = HasherSettings()


settings = TestSettings()
