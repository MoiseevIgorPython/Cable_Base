from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from models.users import User


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Зависимость для работы с базой данных пользователей."""
    yield SQLAlchemyUserDatabase(session, User)
