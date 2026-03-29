from typing import AsyncGenerator

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (declarative_base, declarative_mixin, declared_attr,
                            mapped_column, sessionmaker)

import events  # noqa

from .config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True, autoincrement=True)


@declarative_mixin
class ComponentName:
    name = mapped_column(String(64))


Base = declarative_base(cls=PreBase)


engine = create_async_engine(settings.async_database_url, echo=True)
async_session = AsyncSession(engine)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as async_session:
        yield async_session
