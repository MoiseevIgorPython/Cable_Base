from fastapi import APIRouter

from core.auth.backend import auth_backend
from schemas.user_schema import UserCreate, UserRead, UserUpdate

from ..dependencies import fastapi_users

auth_router = APIRouter(prefix="/auth",
                        tags=["Authentication"])
user_router = APIRouter(prefix="/users",
                        tags=["Users"])

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend,
                                  # requires_verification=True
                                  ),
    prefix="/jwt")

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate))

# main_router.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"])

auth_router.include_router(
    fastapi_users.get_reset_password_router())

user_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate))
