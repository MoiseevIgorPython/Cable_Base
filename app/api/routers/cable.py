from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import construction_exist
from app.core.db import get_async_session
from app.models import Cable

from app.schemas.cable_schema import CableDB, CableCreate


cable_router = APIRouter(prefix='/cable',
                         tags=['cable'],)


@cable_router.get('/',
                  response_model=list[CableDB])
async def get_cable(session: AsyncSession = Depends(get_async_session)):
    cables = await session.execute(select(Cable))
    return cables.scalars().all()


@cable_router.post('/',
                   response_model=CableDB)
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
