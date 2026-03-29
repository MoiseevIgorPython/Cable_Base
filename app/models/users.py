from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users.db import (SQLAlchemyBaseUserTable,
                              SQLAlchemyBaseUserTableUUID,
                              SQLAlchemyUserDatabase)
from sqlalchemy import (BigInteger, CheckConstraint, Computed, Float,
                        ForeignKey, Integer, String, UniqueConstraint)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from core.db import Base, get_async_session


class User(Base, SQLAlchemyBaseUserTable):  # SQLAlchemyBaseUserTableUUID
    tg_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


SECRET = "SECRET"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(name="jwt",
                                     transport=bearer_transport,
                                     get_strategy=get_jwt_strategy,)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    reset_password_token_lifetime_seconds = 4200

    async def on_after_register(self, user: User, request: Request | None = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
