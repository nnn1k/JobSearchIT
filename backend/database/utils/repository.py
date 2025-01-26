from typing import List, Dict, Optional, Literal

from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload, selectinload

from backend.database.settings.database import session_factory, Base
from datetime import datetime, timedelta

class RepositoryHelper:

    async def get_model(self, session, **kwargs):
        model_id = kwargs.pop('id', None)
        if model_id is None:
            return None
        return await session.get(self.db_model, model_id)

    async def model_to_schema(self, model):
        return self.schema.model_validate(model, from_attributes=True)

    async def get_query(self, session, kwargs):
        query = (
            select(self.db_model)
            .filter_by(**kwargs)
        )
        return await session.execute(query)

class AlchemyRepository(RepositoryHelper):

    db_model: Base = None
    schema: BaseModel = None

    async def get_all(self, **kwargs) -> Optional[List[BaseModel]]:
        async with session_factory() as session:
            res = await self.get_query(session, kwargs)
            models = res.scalars().all()
            if models is None:
                return None
            return [await self.model_to_schema(model) for model in models]

    async def get_one(self, **kwargs) -> Optional[BaseModel]:
        async with session_factory() as session:
            res = await self.get_query(session, kwargs)
            model = res.scalars().one_or_none()
            if model is None:
                return None
            return await self.model_to_schema(model)

    async def add_one(self, **kwargs) -> Optional[BaseModel]:
        async with session_factory() as session:
            query = (
                insert(self.db_model)
                .values(**kwargs)
                .returning(self.db_model)
            )
            res = await session.execute(query)

            model = res.scalars().one_or_none()
            new_model = await self.model_to_schema(model)
            await session.commit()

            return new_model

    async def update_one(self, **kwargs) -> Optional[BaseModel]:
        async with session_factory() as session:
            model = await self.get_model(session, **kwargs)
            if model is None:
                print({'error': 'model is missing'})
                return None

            for key, value in kwargs.items():
                setattr(model, key, value)
            new_model = await self.model_to_schema(model)
            await session.commit()
            return new_model

    async def delete_one(self, **kwargs) -> Optional[Dict[str, bool]]:
        async with session_factory() as session:
            model = await self.get_model(session, **kwargs)
            if model is None:
                print({'error': 'model is missing'})
                return None

            await session.delete(model)
            await session.commit()

            return {'deleted': True}

    async def soft_delete(self, id: int, type_action: Literal['delete', 'restore']) -> Optional[BaseModel]:
        async with session_factory() as session:
            model = await self.get_model(session, id=id)
            if model is None:
                print({'error': 'model is missing'})
                return None
            match type_action:
                case 'delete':
                    model.deleted_at = datetime.utcnow() + timedelta(hours=3)
                case 'restore':
                    model.deleted_at = None

            new_model = await self.model_to_schema(model)
            await session.commit()
            return new_model
