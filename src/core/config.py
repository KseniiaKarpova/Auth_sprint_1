from logging import config as logging_config
from core.logger import LOGGING
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

logging_config.dictConfig(LOGGING)


class PostgresDbSettings(BaseSettings):
    host: str = ...
    user: str = ...
    port: int = ...
    db: str = ...
    password: str = ...

    model_config = SettingsConfigDict(env_prefix='postgres_')


class APPSettings(BaseSettings):
    project_name: str = 'Auth API'

    db: PostgresDbSettings = PostgresDbSettings()
    db_dsn: str = f'postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.db}'


settings = APPSettings()
