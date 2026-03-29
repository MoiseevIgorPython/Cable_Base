from pydantic import BaseModel

from .base_schema import MetallDB


class TwistBase(BaseModel):
    count_wires: int
    diametr_wires: float
    resistance: float
    step: float

    class Config:
        from_attributes = True
        extra = "ignore"


class TwistDB(TwistBase):
    metall: MetallDB


class TwistCreate(TwistBase):
    metall_id: int
