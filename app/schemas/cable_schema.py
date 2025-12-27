from pydantic import BaseModel
from typing import Optional
from app.schemas.base_schema import AlumoflexDB, DrennageDB, ColorDB, MarkerDB, PlasticDB
from app.schemas.construction_schema import ConstructionDB
from app.schemas.isolation_schema import IsolationDB


class CableBase(BaseModel):
    article: int
    outer_diametr: float
    inner_diametr: float
    radial: float


class CableDB(CableBase):
    isolation: IsolationDB
    construction: ConstructionDB
    drennage: DrennageDB
    alumoflex: AlumoflexDB
    marker: Optional[MarkerDB] = None

    class Config:
        from_attributes = True


class CableCreate(CableBase):
    isolation_id: int
    construction_id: int
    drennage_id: int
    alumoflex_id: int
    marker_id: Optional[int] = None
