from pydantic import BaseModel

from app.schemas.twist_schema import TwistDB


class IsolationBase(BaseModel):
    twist_id: int
    outer_diametr: float
    inner_diametr: float
    twist: TwistDB

    class Config:
        from_attributes = True
        extra = "ignore"


class IsolationDB(IsolationBase):
    id: int
    core: str
    radial: float


class IsolationCreate(IsolationBase):
    pass
