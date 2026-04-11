from typing import Optional

from api.dependencies import current_superuser, current_user
from core.db import get_async_session
from crud.crud_cable import twisting_crud
from fastapi import APIRouter, Depends
from models import Twisting
from models.users import User
from pydantic import BaseModel
from schemas.twist_schema import TwistCreate, TwistDB
from sqlalchemy.ext.asyncio import AsyncSession

from ..validators import object_by_data_exist, object_by_id_not_found


class TwistFilter(BaseModel):
    metall: Optional[str] = None
    count_wires: Optional[int] = None
    diametr_wires: Optional[float] = None


twist_router = APIRouter(prefix='/twist',
                         tags=['twist'],)


@twist_router.get('/', response_model=list[TwistDB])
async def get_twist(skip: int = 0,
                    limit: int = 100,
                    filters: TwistFilter = Depends(),
                    session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)
                    ):
    filter_dict = filters.dict(exclude_unset=True, exclude_none=True)
    twistes = await twisting_crud.get_multi(session,
                                            skip=skip,
                                            limit=limit,
                                            **filter_dict)
    return twistes


@twist_router.post('/',
                   response_model=TwistDB)
async def post_twist(obj_in: TwistCreate,
                     session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_superuser)):
    new_twist = await object_by_data_exist(Twisting, obj_in, session)
    session.add(new_twist)
    await session.commit()
    await session.refresh(new_twist)
    return new_twist


@twist_router.delete('/{core_id}',)
async def delete_twist(core_id: int,
                       session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_superuser)):
    deleting_twist = await object_by_id_not_found(Twisting, core_id, session)
    await session.delete(deleting_twist)
    await session.commit()
    return {"status": "Twist deleted successfully"}
