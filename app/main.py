import uvicorn
from fastapi import FastAPI

from api.routers import main_router

app = FastAPI(docs_url='/swagger')

app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        )
