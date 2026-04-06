from typing import Type, TypeVar

from api.dependencies import current_superuser, current_user
from core.db import get_async_session
from crud.base_crud import BaseCRUD
from fastapi import APIRouter, Body, Depends
from models import Alumoflex, Color, Drennage, Marker, Metall, Plastic
from models.users import User
from pydantic import BaseModel
from schemas.base_schema import (AlumoflexCreate, AlumoflexDB, ColorCreate,
                                 ColorDB, DrennageCreate, DrennageDB,
                                 MarkerCreate, MarkerDB, MetallCreate,
                                 MetallDB, PlasticCreate, PlasticDB)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)


components_router = APIRouter(prefix='/components')


def create_router(model_name: str,
                  db_model: ModelType,
                  create_schema: Type[CreateSchemaType],
                  response_schema: Type[ResponseSchemaType]
                  ) -> APIRouter:

    router = APIRouter(prefix=f'/{model_name}', tags=[model_name])
    crud = BaseCRUD(db_model)

    @router.get('/', response_model=list[response_schema])
    async def get_component(skip: int = 0,
                            limit: int = 100,
                            session: AsyncSession = Depends(
                                get_async_session),
                            user: User = Depends(current_user)):
        objects = await crud.get_multi(session,
                                       skip=skip,
                                       limit=limit)
        return objects

    @router.post('/', response_model=response_schema)
    async def post_component(
        component_data: create_schema = Body(
            ...,
            description="Данные для создания"),
            session: AsyncSession = Depends(get_async_session),
            user: User = Depends(current_superuser)):
        return await crud.create(component_data,
                                 session)

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
components_router.include_router(create_router(model_name='metall',
                                               db_model=Metall,
                                               create_schema=MetallCreate,
                                               response_schema=MetallDB))
