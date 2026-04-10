from enum import Enum

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class UserRole(str, Enum):
    """Роли пользователей."""

    ADMIN = "admin"
    USER = "user"


class Department(str, Enum):
    CABLE = "Кабельный цех."
    TWIST = "Цех скрутки"


class User(Base, SQLAlchemyBaseUserTable):
    """Модель пользователя."""

    tg_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    second_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(UserRole),
        default=UserRole.USER,
        nullable=False)
    department: Mapped[Department] = mapped_column(
        SQLAlchemyEnum(Department),
        nullable=True)
