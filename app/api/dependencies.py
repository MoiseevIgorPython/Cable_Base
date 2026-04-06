from core.auth.backend import auth_backend
from core.auth.db import get_user_db
from core.auth.manager import UserManager
from fastapi import Depends
from fastapi_users import FastAPIUsers
from models.users import User


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend])


current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
