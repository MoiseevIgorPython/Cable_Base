import re
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import BaseValidator, validate_name
from app.core.db import get_async_session
from app.models.cable import (Alumoflex, Cable, Color, Drennage, Marker, Plastic)
from app.schemas.base_schema import (AlumoflexDB, DrennageDB, MarkerDB, PlasticDB, ColorDB,
                                     AlumoflexCreate, DrennageCreate, MarkerCreate, PlasticCreate, ColorCreate)

components_router = APIRouter(prefix='/components', tags=['components'])


#========================================================================Alumoflex
@components_router.get('/alumoflex',
                       response_model=list[AlumoflexDB]
                       )
async def get_alumoflex(session: AsyncSession = Depends(get_async_session)):
    alumoflex = await session.execute(select(Alumoflex))
    return alumoflex.scalars().all()


@components_router.post('/alumoflex',
                        response_model=AlumoflexDB
                        )
async def post_alumoflex(obj_in: AlumoflexCreate,
                         session: AsyncSession = Depends(get_async_session)):
    obj_in_data = obj_in.dict()
    # await BaseValidator(Alumoflex, 'size').name_is_count(obj_in_data['size'],
    #                                                      session)
    alumoflex = Alumoflex(**obj_in_data)
    session.add(alumoflex)
    await session.commit()
    await session.refresh(alumoflex)
    return alumoflex


#========================================================================Drennage
@components_router.get('/drennage',
                       response_model=list[DrennageDB])
async def get_drennage(session: AsyncSession = Depends(get_async_session)):
    drennage = await session.execute(select(Drennage))
    return drennage.scalars().all()


@components_router.post('/drennage',
                        response_model=DrennageDB
                        )
async def create_drennage(obj_in: DrennageCreate,
                          session: AsyncSession = Depends(get_async_session)):
    obj_in_data = obj_in.dict()
    validate_name(obj_in_data['name'])
    # await BaseValidator(Drennage, 'name').name_is_count(obj_in_data['name'],
    #                                                     session)
    drennage = Drennage(**obj_in_data)
    session.add(drennage)
    await session.commit()
    await session.refresh(drennage)
    return drennage


#========================================================================Plastic
@components_router.get('/plastic',
                       response_model=list[PlasticDB])
async def get_plastic(session: AsyncSession = Depends(get_async_session)):
    plastic = await session.execute(select(Plastic))
    return plastic.scalars().all()


@components_router.post('/plastic',
                        response_model=PlasticDB
                        )
async def create_plastic(obj_in: PlasticCreate,
                         session: AsyncSession = Depends(get_async_session)):
    obj_in_data = obj_in.dict()
    # await BaseValidator(Plastic, 'name').name_is_count(obj_in_data['name'],
    #                                                    session)
    plastic = Plastic(**obj_in_data)
    session.add(plastic)
    await session.commit()
    await session.refresh(plastic)
    return plastic


#========================================================================Color
@components_router.get('/color',
                       response_model=list[ColorDB])
async def get_color(session: AsyncSession = Depends(get_async_session)):
    color = await session.execute(select(Color))
    return color.scalars().all()


@components_router.post('/color',
                        response_model=ColorDB
                        )
async def create_color(obj_in: ColorCreate,
                       session: AsyncSession = Depends(get_async_session)):
    obj_in_data = obj_in.dict()
    # await BaseValidator(Color, 'name').name_is_count(obj_in_data['name'],
    #                                                  session)
    color = Color(**obj_in_data)
    session.add(color)
    await session.commit()
    await session.refresh(color)
    return color


#========================================================================Marker
@components_router.get('/marker',
                       response_model=list[MarkerDB])
async def get_marker(session: AsyncSession = Depends(get_async_session)):
    marker = await session.execute(select(Marker))
    return marker.scalars().all()


@components_router.post('/marker',
                        response_model=MarkerDB)
async def create_marker(obj_in: MarkerCreate,
                        session: AsyncSession = Depends(get_async_session)):
    obj_in_data = obj_in.dict()
    # await BaseValidator(Marker, 'name').name_is_count(obj_in_data['name'], session)
    marker = Marker(**obj_in_data)
    session.add(marker)
    await session.commit()
    await session.refresh(marker)
    return marker


#========================================================================Metall
#@components_router.get('/metall',
#                       response_model=list[BaseDB])
#async def get_metall(session: AsyncSession = Depends(get_async_session)):
#    metall = await session.execute(select(Metall))
#    return metall.scalars().all()


#@components_router.post('/metall',
#                        response_model=BaseDB)
#async def create_metall(obj_in: BaseCreate,
#                        session: AsyncSession = Depends(get_async_session)):
#    obj_in_data = obj_in.dict()
#    await BaseValidator(Metall, 'name').name_is_count(obj_in_data['name'],
#                                                      session)
#    new_metall = Metall(**obj_in_data)
#    session.add(new_metall)
#    await session.commit()
#    await session.refresh(new_metall)
#    return new_metall
