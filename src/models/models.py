import uuid

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column)


metadata = MetaData()


class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata


class User(Base):
    __tablename__ = 'users'

    uuid = Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4(),
                                             primary_key=True)
    login = Mapped[str] = mapped_column(nullable=False, unique=True)
    email = Mapped[str] = mapped_column(nullable=False, unique=True)
    password = Mapped[str] = mapped_column(nullable=False)
    name = Mapped[str] = mapped_column(nullable=True)
    surname = Mapped[str] = mapped_column(nullable=True)






"""
After created a table make migration by:
 alembic revision --autogenerate -m 'Name of migration(Created User Table)'
 """
