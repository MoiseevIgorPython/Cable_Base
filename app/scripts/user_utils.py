from typing import Optional

from core.db import AsyncSessionLocal
from fastapi_users.password import PasswordHelper
from models import User
from sqlalchemy import select

password_helper = PasswordHelper()


async def create_superuser(
    email: str,
    password: str,
    first_name: str = "Admin",
    second_name: str = "Admin",
    tg_id: int = 0
) -> Optional[User]:
    """
    Создаёт суперпользователя (администратора) напрямую через SQLAlchemy.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        existing = result.scalar_one_or_none()
        if existing:
            print(f"⚠️ Суперпользователь {email} уже существует")
            return None
        hashed_password = password_helper.hash(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            is_superuser=True,
            is_active=True,
            tg_id=tg_id,
            first_name=first_name,
            second_name=second_name
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        print(f"✅ Суперпользователь {email} успешно создан!")
        return user
