from http import HTTPStatus
from typing import Any, Optional, TypeVar

from fastapi import HTTPException
from models import Cable, Construction, Metall, Twisting
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeMeta

from .base_crud import BaseCRUD

ModelType = TypeVar('ModelType', bound=DeclarativeMeta)


class CableCRUD(BaseCRUD):
    """CRUD модели Cable."""

    def _apply_filters(self, query: Any, **filters: Any) -> Any:
        for field, value in filters.items():
            if value is not None:
                if field == 'construction' and hasattr(self.model, 'construction'):
                    query = (query
                             .join(self.model.construction)
                             .where(Construction.name == value))
                elif field == 'title':
                    query = (query.where(self.model.title == value))
                elif hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        return query

    async def get(self,
                  article: int,
                  session: AsyncSession) -> Optional[ModelType]:
        result = await session.execute(select(self.model)
                                       .where(self.model.article == article))
        result = result.scalar_one_or_none()
        if result is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                                detail=f'Кабель {article} не найден.')
        return result


class TwistingCRUD(BaseCRUD):
    """CRUD модели Twisting."""

    def _apply_filters(self, query: Any, **filters: Any) -> Any:
        for field, value in filters.items():
            if value is not None:
                if field == 'metall' and hasattr(self.model, 'metall'):
                    query = query.join(
                        self.model.metall).where(Metall.name == value)
                elif hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        return query


class ConstructionCRUD(BaseCRUD):
    pass


cable_crud = CableCRUD(Cable)
construction_crud = ConstructionCRUD(Construction)
twisting_crud = TwistingCRUD(Twisting)
