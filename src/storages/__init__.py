from abc import abstractmethod, ABC
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete, update


class AlchemyBaseStorage(ABC):
    table = None

    def __init__(self, session: AsyncSession = None) -> None:
        self.session = session

    async def generate_query(self, attributes: list[str], conditions: dict) -> table:
        where_condition = and_(*[getattr(self.table, field) == value for field, value in conditions.items()])
        attributes = [getattr(self.table, field) for field in attributes] if attributes else self.table
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
    
    async def get_many(self, conditions: dict, attributes: dict = None) -> list[table]:
        """
        SELECT from self.table by specified attributes. Return many objects
        """
        async with self.session:
            query = await self.generate_query(attributes=attributes, conditions=conditions)
            instance = (await self.session.execute(query)).scalars().all()
        return instance
    
    async def create(self, params: dict) -> table:
        """
        INSERT record
        """
        async with self.session:
            instance = self.table(**params)
            self.session.add(instance)
            await self.session.commit()
        return instance

    async def delete(self, conditions: dict):
        """
        DELETE FROM self.table WHERE conditions
        """
        async with self.session:
            where_condition = and_(*[getattr(self.table, field) == value for field, value in conditions.items()])
            query = delete(self.table).where(where_condition)
            instance = await self.session.execute(query)
            await self.session.commit()
        return instance

    async def update(self, conditions: dict, values: dict):
        """
        UPDATE values.keys() SET values FROM self.table WHERE conditions
        """
        async with self.session:
            where_condition = and_(*[getattr(self.table, field) == value for field, value in conditions.items()])
            query = update(self.table).where(where_condition).values(values)
            instance = await self.session.execute(query)
            await self.session.commit()
        return instance