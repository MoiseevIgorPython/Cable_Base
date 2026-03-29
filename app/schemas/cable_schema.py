from typing import Optional

from pydantic import BaseModel

from .base_schema import AlumoflexDB, DrennageDB, MarkerDB
from .construction_schema import ConstructionDB
from .twist_schema import TwistDB


class CableBase(BaseModel):
    article: int


class CableDB(CableBase):
    title: str
    outer_diametr: float
    inner_diametr: float
    twisting: TwistDB
    construction: ConstructionDB
    drennage: DrennageDB
    alumoflex: AlumoflexDB
    marker: Optional[MarkerDB] = None

    class Config:
        from_attributes = True


class CableCreate(CableBase):
    twist_id: int
    construction_id: int
    drennage_id: int
    alumoflex_id: int
    marker_id: Optional[int] = None
