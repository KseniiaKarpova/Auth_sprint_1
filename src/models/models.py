import uuid

from sqlalchemy import ForeignKey, MetaData, types
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

metadata = MetaData()


class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata


class User(Base):
    __tablename__ = 'users'

    uuid: Mapped[UUID] = mapped_column(types.Uuid,
                                       default=uuid.uuid4,
                                       primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=True)
    surname: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)  # instead deleting user, change this field
    user_role: Mapped['UserRole'] = relationship(back_populates='users',
                                                 cascade='all, delete',
                                                 passive_deletes=True)
    user_history: Mapped['UserHistory'] = relationship(back_populates='user_history',
                                                       cascade='all, delete',
                                                       passive_deletes=True)


class Role(Base):
    __tablename__ = 'roles'

    uuid: Mapped[UUID] = mapped_column(types.Uuid,
                                       default=uuid.uuid4,
                                       primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)


class UserRole(Base):
    __tablename__ = 'users_roles'

    uuid: Mapped[UUID] = mapped_column(types.Uuid,
                                       default=uuid.uuid4,
                                       primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.uuid'),
                                          onupdate='CASCADE',
                                          nullable=False)
    role_id: Mapped[UUID] = mapped_column(ForeignKey('roles.uuid'),
                                          onupdate='CASCADE',
                                          nullable=False)
    user: Mapped['User'] = relationship(back_populates='users_roles')
    role: Mapped['Role'] = relationship(back_populates='users_roles')


class UserHistory(Base):
    __tablename__ = 'user_history'

    uuid: Mapped[UUID] = mapped_column(types.Uuid,
                                       default=uuid.uuid4,
                                       primary_key=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.uuid'),
                                          onupdate='CASCADE',
                                          nullable=False)

    user_agent: Mapped[str] = mapped_column(nullable=True)
    refresh_token: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    user: Mapped['User'] = relationship(back_populates='user_history')


"""
After created a table make migration by:
 alembic revision --autogenerate -m 'Name of migration(Created User Table)'
"""
