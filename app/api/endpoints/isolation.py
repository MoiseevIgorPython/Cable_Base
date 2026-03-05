from core.db import get_async_session
from fastapi import APIRouter, Depends
from models import Isolation, Twisting
from schemas.isolation_schema import IsolationCreate, IsolationDB
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..validators import object_by_id_not_found, objects_not_found

isolation_router = APIRouter(prefix='/isolation',
                             tags=['isolation'],)


@isolation_router.get('/',
                      response_model=list[IsolationDB])
async def get_isolation(session: AsyncSession = Depends(get_async_session)):
    return await objects_not_found(Isolation, session)


@isolation_router.post('/',
                       response_model=IsolationDB)
async def post_core(obj_in: IsolationCreate,
                    session: AsyncSession = Depends(get_async_session)):
    obj_in_data = obj_in.dict()
    twist = await session.execute(select(Twisting).where(Twisting.id == obj_in_data['twist_id']))
    twist = twist.scalars().first()
    core_description = f'{twist.count_wires}x{twist.diametr_wires}{twist.metall.name[0].lower()}'
    obj_in_data['core'] = core_description
    new_core = Isolation(**obj_in_data)
    session.add(new_core)
    await session.commit()
    await session.refresh(new_core)
    return new_core


@isolation_router.delete('/{core_id}',)
async def delete_core(core_id: int,
                      session: AsyncSession = Depends(get_async_session)):
    deleting_core = await object_by_id_not_found(Isolation, core_id, session)
    await session.delete(deleting_core)
    await session.commit()
    return {"status": "Core deleted successfully"}
