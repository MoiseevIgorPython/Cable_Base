from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_

# from app.api.validators import object_not_found
from core.db import get_async_session
from models import Cable, Construction, Isolation
from schemas.cable_schema import CableCreate, CableDB


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
                   response_model=CableDB
                   )
async def post_cable(obj_in: CableCreate,
                     session: AsyncSession = Depends(get_async_session)):
    obj_in_data = obj_in.dict()
    cable = Cable(**obj_in_data)
    session.add(cable)
    await session.commit()
    await session.refresh(cable)
    return cable


@cable_router.get('/{cable_id}/',
                  response_model=CableDB)
async def get_cable_by_id(cable_id: int,
                          session: AsyncSession = Depends(get_async_session)):
    cable = await session.execute(select(Cable).where(Cable.id == cable_id))
    cable = cable.scalar_one_or_none()
    if not cable:
        raise HTTPException(status_code=404, detail="Cable not found")
    return cable


@cable_router.delete('/{cable_id}')
async def delete_cable(cable_id: int,
                       session: AsyncSession = Depends(get_async_session)):
    cable = await session.execute(select(Cable).where(Cable.id == cable_id))
    deleting_cable = cable.scalars().first()
    await session.delete(deleting_cable)
    await session.commit()
    return {"status": "Cable deleted successfully"}
