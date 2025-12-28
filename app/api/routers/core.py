import re
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.validators import BaseValidator, object_exist, validate_name
from app.core.db import get_async_session
from app.models import Isolation
from app.schemas.isolation_schema import IsolationDB, IsolationBase, IsolationCreate
# from app.schemas.core_schemas import CoreCreate, CoreDB

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
    new_core = Isolation(**obj_in_data)
    # validate_name(obj_in_data['name'])
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
