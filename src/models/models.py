import uuid

from sqlalchemy import MetaData, types, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            relationship)

metadata = MetaData()


class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata


class User(Base):
    __tablename__ = 'users'

    uuid: Mapped[uuid.UUID] = mapped_column(types.UUID,
                                            default=uuid.uuid4,
                                            primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=True)
    surname: Mapped[str] = mapped_column(nullable=True)
    user_role: Mapped['UserRole'] = relationship(back_populates='users',
                                                 cascade='all, delete',
                                                 passive_deletes=True)


class Role(Base):
    __tablename__ = 'roles'

    uuid: Mapped[uuid.UUID] = mapped_column(types.UUID,
                                            default=uuid.uuid4,
                                            primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)


class UserRole(Base):
    __tablename__ = 'users_roles'

    uuid: Mapped[uuid.UUID] = mapped_column(types.UUID,
                                            default=uuid.uuid4,
                                            primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.uuid'),
                                               onupdate='CASCADE',
                                               ondelete='CASCADE',
                                               nullable=False)
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('roles.uuid'),
                                               onupdate='CASCADE',
                                               ondelete='CASCADE',
                                               nullable=False)
    user: Mapped['User'] = relationship(back_populates='users_roles')
    role: Mapped['Role'] = relationship(back_populates='users_roles')






"""
After created a table make migration by:
 alembic revision --autogenerate -m 'Name of migration(Created User Table)'
 """
