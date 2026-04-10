import os

from dotenv import load_dotenv
from fastapi_users.password import PasswordHelper
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import and_, select
from starlette.requests import Request

from core.db import AsyncSessionLocal
from models import User

load_dotenv("../.env")

password_helper = PasswordHelper()


class AdminAuth(AuthenticationBackend):
    async def login(self,
                    request: Request
                    ) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        async with AsyncSessionLocal() as session:
            admin_user = await session.execute(
                select(User).where(
                    and_(User.email == username,
                         User.is_superuser,
                         User.is_active)))
            admin_user = admin_user.scalar_one_or_none()
            if admin_user is None:
                return False

            is_valid, updated_hash = password_helper.verify_and_update(
                    password, admin_user.hashed_password)

            if not is_valid:
                return False

            if updated_hash is not None:
                admin_user.hashed_password = updated_hash
                await session.commit()

        request.session.update(
            {"token": os.environ.get("ADMIN_AUTH_TOKEN"),
             "user_id": admin_user.id,
             "email": admin_user.email}
             )

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False
        return True


authentication_backend = AdminAuth(secret_key=os.environ.get("ADMIN_AUTH_BACKEND_SECRET"))
