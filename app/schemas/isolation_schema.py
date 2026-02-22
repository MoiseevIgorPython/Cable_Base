from pydantic import BaseModel

from .twist_schema import TwistDB


class IsolationBase(BaseModel):
    twist_id: int
    outer_diametr: float
    inner_diametr: float

    class Config:
        from_attributes = True
        extra = "ignore"


class IsolationDB(IsolationBase):
    id: int
    core: str
    radial: float
    twist: TwistDB


class IsolationCreate(IsolationBase):
    twist_id: int
