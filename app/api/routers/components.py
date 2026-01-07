import re
from http import HTTPStatus
from typing import Type, TypeVar

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.api.validators import BaseValidator, validate_name
from app.core.db import get_async_session
from app.models import Alumoflex, Color, Drennage, Marker, Plastic
from app.schemas.base_schema import (AlumoflexDB, DrennageDB, MarkerDB, PlasticDB, ColorDB,
                                     AlumoflexCreate, DrennageCreate, MarkerCreate, PlasticCreate, ColorCreate)


ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)


components_router = APIRouter(prefix='/components')


def create_router(model_name: str,
                  db_model: Type[ModelType],
                  create_schema: Type[CreateSchemaType],
                  response_schema: Type[ResponseSchemaType]
                  ) -> APIRouter:

    router = APIRouter(prefix=f'/{model_name}', tags=[model_name])

    @router.get('/', response_model=list[response_schema])
    async def get_component(session: AsyncSession = Depends(get_async_session)):
        component = await session.execute(select(db_model))
        return component.scalars().all()


    @router.post('/', response_model=response_schema)
    async def post_component(obj_in: CreateSchemaType,
                             session: AsyncSession = Depends(get_async_session)):
        obj_in_data = obj_in.dict()
        new_component_obj = db_model(**obj_in_data)
        session.add(new_component_obj)
        await session.commit()
        await session.refresh(new_component_obj)
        return new_component_obj

    return router


components_router.include_router(create_router(model_name='alumoflex',
                                               db_model=Alumoflex,
                                               create_schema=AlumoflexCreate,
                                               response_schema=AlumoflexDB))
components_router.include_router(create_router(model_name='drennage',
                                               db_model=Drennage,
                                               create_schema=DrennageCreate,
                                               response_schema=DrennageDB))
components_router.include_router(create_router(model_name='plastic',
                                               db_model=Plastic,
                                               create_schema=PlasticCreate,
                                               response_schema=PlasticDB))
components_router.include_router(create_router(model_name='color',
                                               db_model=Color,
                                               create_schema=ColorCreate,
                                               response_schema=ColorDB))
components_router.include_router(create_router(model_name='marker',
                                               db_model=Marker,
                                               create_schema=MarkerCreate,
                                               response_schema=MarkerDB))
