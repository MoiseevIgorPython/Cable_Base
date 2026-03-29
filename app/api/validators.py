from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.construction_schema import ConstructionCreate


async def objects_not_found(model,
                            session: AsyncSession):
    """Проверка - добавлен ли хотябы 1 объект."""
    objects = await session.execute(select(model))
    objects = objects.scalars().all()
    if objects == []:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=f'Объект {model.__name__} пока не создан.')
    return objects


async def object_by_id_not_found(model,
                                 obj_id: int,
                                 session: AsyncSession):
    """Проверка существования объекта по id."""
    current_object = await session.execute(select(model)
                                           .where(model.id == obj_id))
    current_object = current_object.scalars().first()
    if current_object is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=f'Объект {model.__name__} не найден.')
    return current_object


async def object_by_data_exist(model,
                               obj_in: ConstructionCreate,
                               session: AsyncSession):
    """Проверка существует ли объект с такими же данными."""
    obj_in_data = obj_in.dict(exclude_unset=True)
    conditions = []
    for field, value in obj_in_data.items():
        if hasattr(model, field):
            conditions.append(getattr(model, field) == value)
    if not conditions:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail='Обязательные поля не переданы.')
    result = await session.execute(select(model).where(and_(*conditions)))
    result_scalar = result.scalar_one_or_none()
    if result_scalar is not None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail='Объект с такими данными уже существует.')
    return model(**obj_in_data)
