from api import (auth_router, cable_router, components_router,
                 construction_router, twist_router, user_router)
from fastapi import APIRouter

main_router = APIRouter(prefix="/api")

main_router.include_router(cable_router)
main_router.include_router(twist_router)
main_router.include_router(construction_router)
main_router.include_router(components_router)
main_router.include_router(auth_router)
main_router.include_router(user_router)
