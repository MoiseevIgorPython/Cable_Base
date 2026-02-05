import uvicorn
from fastapi import FastAPI

from app.api.routers.cable import cable_router
from app.api.routers.components import components_router
from app.api.routers.construction import construction_router
from app.api.routers.core import isolation_router
from app.api.routers.twist import twist_router

app = FastAPI(docs_url='/swagger')


app.include_router(construction_router, prefix='/api')
app.include_router(cable_router, prefix='/api')
app.include_router(isolation_router, prefix='/api')
app.include_router(twist_router, prefix='/api')
app.include_router(components_router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run(
        'app.main:app',
        host='0.0.0.0',
        port=8000)
