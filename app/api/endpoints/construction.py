from core.db import get_async_session
from fastapi import APIRouter, Depends
from models import Construction
from schemas.construction_schema import ConstructionCreate, ConstructionDB
from sqlalchemy.ext.asyncio import AsyncSession

from ..validators import (object_by_data_exist, object_by_id_not_found,
                          objects_not_found)

construction_router = APIRouter(prefix='/construction',
                                tags=['construction'],)


@construction_router.get('/',
                         response_model=list[ConstructionDB])
async def get_construction(session: AsyncSession = Depends(get_async_session)):
    return await objects_not_found(Construction, session)


@construction_router.post('/',
                          response_model=ConstructionDB)
async def create_construction(obj_in: ConstructionCreate,
                              session: AsyncSession = Depends(
                                  get_async_session)):
    new_construction = await object_by_data_exist(Construction,
                                                  obj_in,
                                                  session)
    session.add(new_construction)
    await session.commit()
    await session.refresh(new_construction)
    return new_construction


@construction_router.delete('/{id}')
async def delete_construction(id: int,
                              session: AsyncSession = Depends(
                                  get_async_session)):
    construction = await object_by_id_not_found(Construction, id, session)
    await session.delete(construction)
    await session.commit()
    return {"status": "Construction deleted successfully"}
