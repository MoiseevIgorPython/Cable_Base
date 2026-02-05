from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import object_not_found
from app.core.db import get_async_session
from app.models import Twisting
from app.schemas.twist_schema import TwistCreate, TwistDB

twist_router = APIRouter(prefix='/twist',
                         tags=['twist'],)


@twist_router.get('/',
                  response_model=list[TwistDB])
async def get_twist(session: AsyncSession = Depends(get_async_session)):
    twistes = await session.execute(select(Twisting))
    return twistes.scalars().all()


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
