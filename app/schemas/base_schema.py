from typing import Optional

from pydantic import BaseModel


class BaseDB(BaseModel):
    name: str

    class Config:
        from_attributes = True


class MarkerDB(BaseModel):
    id: Optional[int] = None
    text: str

    class Config:
        from_attributes = True


class AlumoflexDB(BaseDB):
    pass


class PlasticDB(BaseDB):
    pass


class DrennageDB(BaseDB):
    pass


class ColorDB(BaseDB):
    pass


class AlumoflexCreate(BaseDB):
    pass


class PlasticCreate(BaseDB):
    pass


class DrennageCreate(BaseDB):
    pass


class ColorCreate(BaseDB):
    pass


class MarkerCreate(MarkerDB):
    pass


class MetallDB(BaseDB):
    pass


class MetallCreate(BaseDB):
    pass
