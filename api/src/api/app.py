from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from .routers.usuario_router import router as usuario_router
from .routers.organizacion_router import router as organizacion_router
from .routers.evento_router import router as evento_router
from .routers.suscripcion_router import router as suscripcion_router
from .database import engine
from .models import anidados, evento_modelo, organizacion_modelo, suscripcion_modelo, usuario_modelo


app = FastAPI()

app.title = "Practico 7 - Tablas Relacionadas"

app.include_router(usuario_router)
app.include_router(organizacion_router)
app.include_router(evento_router)
app.include_router(suscripcion_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # cambiar antes de presentar la EFI
    allow_credentials = False,
    allow_methods=["*"],
    allow_headers=["*"]
)


add_pagination(app)


SQLModel.metadata.create_all(bind = engine)
