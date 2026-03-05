from typing import Any, Dict, List, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeMeta

ModelType = TypeVar('ModelType', bound=DeclarativeMeta)


class BaseCRUD:

    def __init__(self, model):
        self.model = model

    def _apply_filters(self, query: Any, **filters: Any) -> Any:
        for field, value in filters.items():
            if hasattr(self.model, field) and value is not None:
                query = query.where(getattr(self.model, field) == value)
        return query

    async def get_multi(self,
                        session: AsyncSession,
                        skip: int = 0,
                        limit: int = 100,
                        **filters: Any) -> List[ModelType]:
        query = select(self.model)
        query = self._apply_filters(query, **filters)
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def get(self,
                  id: int,
                  session: AsyncSession) -> Optional[ModelType]:
        result = await session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def update(self,
                     db_obj: ModelType,
                     update_data: Dict[str, Any],
                     session: AsyncSession) -> ModelType:
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self,
                     db_obj: ModelType,
                     session: AsyncSession) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
