from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from .routers.usuario_router import router as articulo_router
from .routers.organizacion_router import router as proveedor_router
from .routers.evento_router import router as evento_router
from .database import engine
from .models.modelos import Usuario, Organizacion, Evento


app = FastAPI()

app.title = "Practico 7 - Tablas Relacionadas"

app.include_router(articulo_router)
app.include_router(proveedor_router)
app.include_router(evento_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # cambiar antes de presentar la EFI
    allow_credentials = False,
    allow_methods=["*"],
    allow_headers=["*"]
)


SQLModel.metadata.create_all(bind = engine)