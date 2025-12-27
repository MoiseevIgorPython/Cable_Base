from typing import AsyncGenerator

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (declarative_base, declarative_mixin, declared_attr,
                            sessionmaker)

from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)


@declarative_mixin
class ComponentName:
    name = Column(String(64))


Base = declarative_base(cls=PreBase)


engine = create_async_engine(settings.database_url, echo=True)

async_session = AsyncSession(engine)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession) 

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as async_session:
        yield async_session
