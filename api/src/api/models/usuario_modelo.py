from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

from .organizacion_modelo import Organizacion


class UsuarioBase(SQLModel):
    nombre: str
    rol: str = "UsuarioNoRegistrado" # UsuarioNoRegistrado, UsuarioRegistrado o Admin (para React)
    fecha_nacimiento: datetime
    suscripciones: list[str] | None = None
    organizacion_id: list[Organizacion] | None = Field(default = None, foreign_key = "organizacion.id")


class Usuario(UsuarioBase, table = True):
    id: int | None = Field(default = None, primery_key = True)
    organizacion: Organizacion | None = Relationship(back_populates = "usuario")
    contrasenia: str


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioPublic(UsuarioBase):
    id: int
