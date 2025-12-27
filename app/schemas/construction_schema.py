from pydantic import BaseModel
from .base_schema import ColorDB, PlasticDB


class ConstructionBase(BaseModel):
    name: str


class ConstructionDB(ConstructionBase):
    color: ColorDB
    isolate_plastic: PlasticDB
    shell_plastic: PlasticDB


class ConstructionCreate(ConstructionBase):
    color_id: int
    isolate_plastic_id: int
    shell_plastic_id: int