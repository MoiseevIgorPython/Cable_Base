import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from models.users import User

load_dotenv(".env")

SECRET = os.environ.get("SECRET", "default_secret_key_for_dev")


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    reset_password_token_lifetime_seconds = 4200

    async def on_after_register(self, user: User,
                                request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    # async def on_after_forgot_password(
    #     self, user: User, token: str, request: Request | None = None
    # ):
    #     print(f"User {user.id} has forgot their password. Reset token: {token}")

    # async def on_after_request_verify(
    #     self, user: User, token: str, request: Request | None = None
    # ):
    #     print(f"Verification requested for user {user.id}. Verification token: {token}")
