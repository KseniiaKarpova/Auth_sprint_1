from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

metadata = MetaData()


class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata


class SomeClass(Base):
    pass


"""
After created a table make migration by:
 alembic revision --autogenerate -m 'Name of migration(Created User Table)'
 """
