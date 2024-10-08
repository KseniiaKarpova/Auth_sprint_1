from abc import ABC
from sqlalchemy import and_, select, update, desc, asc
from sqlalchemy.orm import Query
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Base
from exceptions import order_by_field_not_found
from sqlalchemy.exc import IntegrityError
from exceptions import integrity_error


class AlchemyBaseStorage(ABC):
    table: Base = None

    def __init__(
            self, session: AsyncSession = None,
            limit: int = 10,
            offset: int = 1,
            order_by: list[str] = ['-created_at']) -> None:
        self.session = session
        self.limit = limit
        self.offset = offset
        self.order_by = order_by

    async def desc_or_asc(self, field_name: str):
        try:
            if field_name[0] == "-":
                return desc, field_name.replace('-', '')
        except IndexError:
            raise 
        return asc, field_name

    async def get_attribute(self, field_name: str):
        try:
            return getattr(self.table, field_name)
        except AttributeError:
            raise order_by_field_not_found

    async def order(self):
        query: Query = getattr(self, 'query', None)
        order_by = list()
        for field_name in self.order_by:
            operator, field_name = await self.desc_or_asc(field_name)
            table_field = await self.get_attribute(field_name)
            order_by.append(operator(table_field))

        if not self.order_by:
            order_by = [desc(self.table.created_at)]

        setattr(self, 'query', query.order_by(*order_by))

    async def paginate(self):
        query: Query = getattr(self, 'query', None)
        setattr(self, 'query', query.limit(self.limit).offset(self.offset))
    
    async def select_actives(self, conditions: dict):
        conditions.update({
            'is_active': True
        })
        return conditions

    async def generate_where(self, conditions: dict):
        conditions = await self.select_actives(conditions)
        return and_(*[getattr(self.table, field) == value for field, value in conditions.items()])

    async def schoose_attributes(self, attributes: list[str]):
        return [getattr(self.table, field) for field in attributes] if attributes else self.table

    async def generate_query(self, conditions: dict, attributes: dict = None) -> table:
        where_condition = await self.generate_where(conditions)
        attributes: [self.table] = await self.schoose_attributes(attributes)
        return select(attributes).where(where_condition)

    async def exists(self, conditions: dict, attributes: dict = None) -> table:
        async with self.session:
            query = await self.generate_query(attributes=attributes, conditions=conditions)
            instance = (await self.session.execute(query)).scalar()
        return bool(instance)

    async def get(self, conditions: dict, attributes: dict = None) -> table:
        """
        SELECT from self.table by specified attributes. Return one objects
        """
        async with self.session:
            query = await self.generate_query(attributes=attributes, conditions=conditions)
            instance = (await self.session.execute(query)).scalar()
        return instance
    
    async def get_many(self, conditions: dict, attributes: dict = None, ) -> list[table]:
        """
        SELECT from self.table by specified attributes. Return many objects
        """
        async with self.session:
            setattr(self, 'query', await self.generate_query(attributes=attributes, conditions=conditions))
            await self.order()
            query: Query = getattr(self, 'query', None)
            instance = (await self.session.execute(query)).scalars().all()
        return instance

    async def create(self, params: dict) -> table:
        """
        INSERT record
        """
        async with self.session:
            instance = self.table(**params)
            self.session.add(instance)
            try:
                await self.session.commit()
            except IntegrityError:
                raise integrity_error
        return instance

    async def delete(self, conditions: dict):
        """
        DO NOT DELETE, MAKE is_active = False
        """
        async with self.session:
            where_condition = await self.generate_where(conditions=conditions)
            query = update(self.table).where(where_condition).values({
                'is_active': False
            })
            instance = await self.session.execute(query)
            await self.session.commit()
        return instance

    async def update(self, conditions: dict, values: dict):
        """
        UPDATE values.keys() SET values FROM self.table WHERE conditions
        """
        async with self.session:
            where_condition = await self.generate_where(conditions=conditions)
            query = update(self.table).where(where_condition).values(values)
            try:
                instance = await self.session.execute(query)
                await self.session.commit()
            except IntegrityError:
                raise integrity_error
        return instance
