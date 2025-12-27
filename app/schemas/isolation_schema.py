from pydantic import BaseModel


class IsolationBase(BaseModel):
    core: str
    outer_diametr: float
    inner_diametr: float
    radial: float

    class Config:
        from_attributes = True
        extra = "ignore"


class IsolationDB(IsolationBase):
    id: int


class IsolationCreate(IsolationBase):
    pass
