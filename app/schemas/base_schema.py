from pydantic import BaseModel
from typing import Optional

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
    id: int

class PlasticDB(BaseDB):
    id: int

class DrennageDB(BaseDB):
    id: int

class ColorDB(BaseDB):
    id: int

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