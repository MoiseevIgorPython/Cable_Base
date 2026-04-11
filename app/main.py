from contextlib import asynccontextmanager

import uvicorn
from admin.admin import (AlumoflexAdmin, CableAdmin, ColorAdmin,
                         ConstructionAdmin, DrennageAdmin, MarkerAdmin,
                         MetallAdmin, PlasticAdmin, TwistingAdmin, UserAdmin)
from admin.admin_auth import authentication_backend
from api.routers import main_router
from core.db import engine
from fastapi import FastAPI
from scripts.user_utils import create_superuser
from sqladmin import Admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Действия при запуске и остановке приложения."""
    print("Starting up...")
    try:
        await create_superuser(email="admin@admin.ru",
                               password="admin123")
        print("✅ Superuser created successfully!")
    except Exception as e:
        print(f"⚠️ Superuser creation error: {e}")
    yield
    print("Shutting down...")


app = FastAPI(docs_url='/swagger', lifespan=lifespan)
admin = Admin(app,
              engine,
              authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(ConstructionAdmin)
admin.add_view(TwistingAdmin)
admin.add_view(CableAdmin)
admin.add_view(ColorAdmin)
admin.add_view(PlasticAdmin)
admin.add_view(MarkerAdmin)
admin.add_view(DrennageAdmin)
admin.add_view(AlumoflexAdmin)
admin.add_view(MetallAdmin)

app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        )
