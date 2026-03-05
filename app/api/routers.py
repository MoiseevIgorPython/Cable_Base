from fastapi import APIRouter

from .endpoints import (cable_router, components_router, construction_router,
                        isolation_router, twist_router)

main_router = APIRouter(prefix='/api')

main_router.include_router(cable_router)
main_router.include_router(isolation_router)
main_router.include_router(twist_router)
main_router.include_router(construction_router)
main_router.include_router(components_router)
