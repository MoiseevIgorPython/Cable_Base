from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import current_superuser, current_user
from core.db import get_async_session
from crud.crud_cable import cable_crud
from models import Cable
from models.users import User
from schemas.cable_schema import CableCreate, CableDB

from ..validators import object_by_data_exist, object_by_id_not_found


class CableFilter(BaseModel):
    article: Optional[int] = None
    construction: Optional[str] = None
    title: Optional[str] = None


cable_router = APIRouter(prefix='/cable',
                         tags=['cable'],)


@cable_router.get('/',
                  response_model=list[CableDB])
async def get_cable(skip: int = 0,
                    limit: int = 100,
                    filters: CableFilter = Depends(),
                    session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)
                    ):
    filter_dict = filters.dict(exclude_unset=True, exclude_none=True)
    cables = await cable_crud.get_multi(session,
                                        skip=skip,
                                        limit=limit,
                                        **filter_dict)
    return cables


@cable_router.post('/',
                   response_model=CableDB)
async def post_cable(obj_in: CableCreate,
                     session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_superuser)
                     ):
    cable = await object_by_data_exist(Cable, obj_in, session)
    session.add(cable)
    await session.commit()
    await session.refresh(cable)
    return cable


@cable_router.get('/{cable_article}/',
                  response_model=CableDB)
async def get_cable_by_article(cable_article: int,
                               session: AsyncSession = Depends(
                                   get_async_session),
                               user: User = Depends(current_user)
                               ):
    return await cable_crud.get(cable_article, session)


@cable_router.delete('/{cable_id}')
async def delete_cable(cable_id: int,
                       session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_superuser)
                       ):
    deleting_cable = await object_by_id_not_found(Cable, cable_id, session)
    await session.delete(deleting_cable)
    await session.commit()
    return {"status": "Cable deleted successfully"}
