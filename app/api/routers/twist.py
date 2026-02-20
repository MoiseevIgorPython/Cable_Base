from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_

from app.api.validators import object_not_found
from app.core.db import get_async_session
from app.models import Metall, Twisting
from app.schemas.twist_schema import TwistCreate, TwistDB


class Filters(BaseModel):
    metall: Optional[str] = None
    count_wires: Optional[int] = None
    diametr_wires: Optional[float] = None


twist_router = APIRouter(prefix='/twist',
                         tags=['twist'],)


@twist_router.get('/',
                  response_model=list[TwistDB])
async def get_twist(filters: Filters = Depends(),
                    session: AsyncSession = Depends(get_async_session)):
    query = select(Twisting)
    conditions = []
    if filters.metall is not None:
        query = query.join(Twisting.metall)
        conditions.append(Metall.name == filters.metall)
    if filters.count_wires is not None:
        conditions.append(Twisting.count_wires == filters.count_wires)
    if filters.diametr_wires is not None:
        conditions.append(Twisting.diametr_wires == filters.diametr_wires)
    if conditions:
        query = query.where(and_(*conditions))
    result = await session.execute(query)
    twistes = result.scalars().all()
    return twistes


@twist_router.post('/',
                   response_model=TwistDB)
async def post_twist(obj_in: TwistCreate,
                     session: AsyncSession = Depends(get_async_session)):
    obj_in_data = obj_in.dict()
    new_twist = Twisting(**obj_in_data)
    session.add(new_twist)
    await session.commit()
    await session.refresh(new_twist)
    return new_twist


@twist_router.delete('/{core_id}',)
async def delete_twist(core_id: int,
                       session: AsyncSession = Depends(get_async_session)):
    deleting_twist = await object_not_found(Twisting, core_id, session)
    await session.delete(deleting_twist)
    await session.commit()
    return {"status": "Twist deleted successfully"}
