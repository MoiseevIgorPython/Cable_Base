from typing import Optional

from fastapi_users import schemas
from models.users import Department, UserRole


class UserRead(schemas.BaseUser[int]):
    tg_id: int
    first_name: str
    second_name: str
    department: Optional[Department]
    role: UserRole


class UserCreate(schemas.BaseUserCreate):
    tg_id: int
    first_name: str
    second_name: str
    # role: str


class UserUpdate(schemas.BaseUserUpdate):
    tg_id: Optional[int]
    first_name: Optional[str]
    second_name: Optional[str]
    department: Optional[Department]
    role: Optional[UserRole]
