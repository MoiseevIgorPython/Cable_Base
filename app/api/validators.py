import re
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cable import (Alumoflex, Cable, Color, Construction, Drennage, Marker, Plastic)


class BaseValidator:
    def __init__(self, model, attr):
        self.model = model
        self.attr = attr

    async def name_is_count(self, value, session: AsyncSession):
        obj = await session.execute(select(self.model).where(getattr(self.model, self.attr) == value))
        obj = obj.scalars().first()
        if obj is not None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='Такой объект уже существует.')


def validate_name(value):
    pattern = r'^\d+\s*[xх]\s*\d+,\d+$'
    if not re.match(pattern, value):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail='Не верный формат')


async def object_exist(obj_id,
                       session: AsyncSession):
    obj = await session.execute(select(Core).where(Core.id == obj_id))
    obj = obj.scalars().first()
    if obj is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Жила не найдена')
    return obj


async def construction_exist(obj_id,
                             session: AsyncSession):
    obj = await session.execute(select(Construction).where(Construction.id == obj_id))
    obj = obj.scalars().first()
    if obj is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Конструкция не найдена')
    return obj


async def number_exist(number,
                       session: AsyncSession):
    obj = await session.execute(select(Construction).where(Construction.number == number))
    obj = obj.scalars().first()
    if obj is not None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail='Такая конструкция уже существует')
    return obj
