from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import Isolation, Twisting
from app.schemas.isolation_schema import (IsolationCreate,
                                          IsolationDB)


isolation_router = APIRouter(prefix='/isolation',
                             tags=['isolation'],)


@isolation_router.get('/',
                      response_model=list[IsolationDB]
                      )
async def get_isolation(session: AsyncSession = Depends(get_async_session)):
    cores = await session.execute(select(Isolation))
    return cores.scalars().all()


@isolation_router.post('/',
                       response_model=IsolationDB)
async def post_core(obj_in: IsolationCreate,
                    session: AsyncSession = Depends(get_async_session)):
    obj_in_data = obj_in.dict()
    # Добавить значение поля core в obj_in_data
    twist = await session.execute(select(Twisting).where(Twisting.id == obj_in_data['twist_id']))
    twist = twist.scalars().first()
    core_description = f'{twist.count_wires}x{twist.diametr_wires}{twist.metall.name[0].lower()}'
    obj_in_data['core'] = core_description
    obj_in_data['radial'] = round((obj_in_data['outer_diametr'] - obj_in_data['inner_diametr']) / 2, 1)
    new_core = Isolation(**obj_in_data)
    session.add(new_core)
    await session.commit()
    await session.refresh(new_core)
    return new_core


@isolation_router.delete('/{core_id}',)
async def delete_core(core_id: int,
                      session: AsyncSession = Depends(get_async_session)):
    # obj = await object_exist(core_id, session)
    core = await session.execute(select(Isolation).where(Isolation.id == core_id))
    deleting_core = core.scalars().first()
    await session.delete(deleting_core)
    await session.commit()
    return {"status": "Core deleted successfully"}
