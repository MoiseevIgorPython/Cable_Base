from typing import Optional

from core.db import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from models import Cable, Construction, Isolation
from pydantic import BaseModel
from schemas.cable_schema import CableCreate, CableDB
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_

from ..validators import (object_by_data_exist, object_by_id_not_found,
                          objects_not_found)


class Filters(BaseModel):
    article: Optional[int] = None
    construction: Optional[str] = None
    core: Optional[str] = None


cable_router = APIRouter(prefix='/cable',
                         tags=['cable'],)


@cable_router.get('/',
                  response_model=list[CableDB])
async def get_cable(filters: Filters = Depends(),
                    session: AsyncSession = Depends(get_async_session)):
    query = select(Cable)
    conditions = []
    if filters.article is not None:
        conditions.append(Cable.article == filters.article)
    if filters.construction is not None:
        query = query.join(Cable.construction)
        conditions.append(Construction.name == filters.construction)
    if filters.core is not None:
        query = query.join(Cable.isolation)
        conditions.append(Isolation.core == filters.core)
    if conditions:
        query = query.where(and_(*conditions))
    result = await session.execute(query)
    cables = result.scalars().all()
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
