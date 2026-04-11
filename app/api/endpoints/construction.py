from api.dependencies import current_superuser, current_user
from core.db import get_async_session
from crud.crud_cable import construction_crud
from fastapi import APIRouter, Depends
from models import Construction
from models.users import User
from schemas.construction_schema import (ConstructionCreate, ConstructionDB,
                                         ConstructionUpdate)
from sqlalchemy.ext.asyncio import AsyncSession

from ..validators import (object_by_data_exist, object_by_id_not_found,
                          objects_not_found)

construction_router = APIRouter(prefix='/construction',
                                tags=['construction'],)


@construction_router.get('/',
                         response_model=list[ConstructionDB])
async def get_construction(session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)):
    return await objects_not_found(Construction, session)


@construction_router.post('/',
                          response_model=ConstructionDB)
async def create_construction(obj_in: ConstructionCreate,
                              session: AsyncSession = Depends(
                                  get_async_session),
                              user: User = Depends(current_superuser)):
    await object_by_data_exist(Construction,
                               obj_in,
                               session)
    return await construction_crud.create(obj_in, session)


@construction_router.get('/{id}',
                         response_model=ConstructionDB)
async def get_construction_by_id(id: int,
                                 session: AsyncSession = Depends(
                                     get_async_session),
                                 user: User = Depends(current_user)):
    await object_by_id_not_found(Construction, id, session)
    return await construction_crud.get(id, session)


@construction_router.delete('/{id}')
async def delete_construction(id: int,
                              session: AsyncSession = Depends(
                                  get_async_session),
                              user: User = Depends(current_superuser)):
    construction = await object_by_id_not_found(Construction, id, session)
    deleted_obj = await construction_crud.remove(construction, session)
    return {"status": "Construction deleted successfully",
            "deleted_obj": deleted_obj}         # доработать вывод


@construction_router.patch('/{id}',
                           response_model=ConstructionDB)
async def update_construction(id: int,
                              obj_in: ConstructionUpdate,
                              session: AsyncSession = Depends(
                                  get_async_session),
                              user: User = Depends(current_superuser)):
    construction = await object_by_id_not_found(Construction, id, session)
    obj_in_data = obj_in.dict(exclude_unset=True, exclude_none=True)
    return await construction_crud.update(construction, obj_in_data, session)
