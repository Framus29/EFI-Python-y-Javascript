from sqlmodel import Field, Relationship, SQLModel
from datetime import date


class UsuarioBase(SQLModel):
    nombre: str
    email: str
    fecha_nacimiento: date


class Usuario(UsuarioBase, table = True):
    id: int | None = Field(default = None, primary_key = True)
    suscripcion: list["Suscripcion"] | None = Relationship(back_populates = "usuario")
    email: str = Field(unique = True)
    contrasenia: str
    rol: str = "Usuario" # Usuario o Admin (para React)


class UsuarioCreate(UsuarioBase):
    contrasenia: str


class UsuarioPublic(UsuarioBase):
    id: int
