from typing import Any

from models import Cable, Construction, Metall, Twisting

from .base_crud import BaseCRUD


class CableCRUD(BaseCRUD):
    """CRUD модели Cable."""

    # def _apply_filters(self, query: Any, **filters: Any) -> Any:
    #     for field, value in filters.items():
    #         if value is not None:
    #             if field == 'construction' and hasattr(self.model, 'construction'):
    #                 query = (query
    #                          .join(self.model.construction)
    #                          .where(Construction.name == value))
    #             elif field == 'core' and hasattr(self.model, 'isolation'):
    #                 query = (query
    #                          .join(self.model.isolation)
    #                          .where(Isolation.core == value))
    #             elif hasattr(self.model, field):
    #                 query = query.where(getattr(self.model, field) == value)
    #     return query


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
