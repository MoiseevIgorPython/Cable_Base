from typing import Optional

from pydantic import BaseModel

from .base_schema import ColorDB, PlasticDB


class ConstructionBase(BaseModel):
    name: str
    radial_isolate: float
    radial_shell: float


class ConstructionDB(ConstructionBase):
    color: ColorDB
    isolate_plastic: PlasticDB
    shell_plastic: PlasticDB


class ConstructionCreate(ConstructionBase):
    color_id: int
    isolate_plastic_id: int
    shell_plastic_id: int


class ConstructionUpdate(BaseModel):
    name: Optional[str] = None
    radial_isolate: Optional[float] = None
    radial_shell: Optional[float] = None
    color_id: Optional[int] = None
    isolate_plastic_id: Optional[int] = None
    shell_plastic_id: Optional[int] = None
