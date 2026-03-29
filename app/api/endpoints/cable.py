from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from crud.crud_cable import cable_crud
from models import Cable
from schemas.cable_schema import CableCreate, CableDB

from ..validators import (object_by_data_exist,
                          object_by_id_not_found)


class CableFilter(BaseModel):
    article: Optional[int] = None
    construction: Optional[str] = None
    core: Optional[str] = None


cable_router = APIRouter(prefix='/cable',
                         tags=['cable'],)


@cable_router.get('/',
                  response_model=list[CableDB])
async def get_cable(skip: int = 0,
                    limit: int = 100,
                    filters: CableFilter = Depends(),
                    session: AsyncSession = Depends(get_async_session)):
    filter_dict = filters.dict(exclude_unset=True, exclude_none=True)
    cables = await cable_crud.get_multi(session,
                                        skip=skip,
                                        limit=limit,
                                        **filter_dict)
    return cables


@cable_router.post('/',
                   response_model=CableDB)
async def post_cable(obj_in: CableCreate,
                     session: AsyncSession = Depends(get_async_session)):
    cable = await object_by_data_exist(Cable, obj_in, session)
    session.add(cable)
    await session.commit()
    await session.refresh(cable)
    return cable


@cable_router.get('/{cable_id}/',
                  response_model=CableDB)
async def get_cable_by_id(cable_id: int,
                          session: AsyncSession = Depends(get_async_session)):
    return await object_by_id_not_found(Cable, cable_id, session)


@cable_router.delete('/{cable_id}')
async def delete_cable(cable_id: int,
                       session: AsyncSession = Depends(get_async_session)):
    deleting_cable = await object_by_id_not_found(Cable, cable_id, session)
    await session.delete(deleting_cable)
    await session.commit()
    return {"status": "Cable deleted successfully"}
