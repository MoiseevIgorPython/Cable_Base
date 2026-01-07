from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import construction_exist, number_exist
from app.core.db import get_async_session
from app.models import Construction
from app.schemas.construction_schema import ConstructionDB, ConstructionCreate


construction_router = APIRouter(prefix='/construction',
                                tags=['construction'],)


@construction_router.get('/',
                         response_model=list[ConstructionDB])
async def get_construction(session: AsyncSession = Depends(get_async_session)):
    constructions = await session.execute(select(Construction))
    return constructions.scalars().all()


@construction_router.post('/',
                          response_model=ConstructionDB
                          )
async def create_construction(obj_in: ConstructionCreate,
                              session: AsyncSession = Depends(get_async_session)):
    obj_in_data = obj_in.dict()
    # await number_exist(obj_in_data['number'], session)
    new_construction = Construction(**obj_in_data)
    session.add(new_construction)
    await session.commit()
    await session.refresh(new_construction)
    return new_construction


@construction_router.delete('/{id}')
async def delete_construction(id: int,
                              session: AsyncSession = Depends(get_async_session)):
    # construction = await construction_exist(id, session)
    construction = await session.execute(
        select(
            Construction).where(
                Construction.id == id))
    deleting_obj = construction.scalars().first()
    await session.delete(deleting_obj)
    await session.commit()
    return {"status": "Construction deleted successfully"}
