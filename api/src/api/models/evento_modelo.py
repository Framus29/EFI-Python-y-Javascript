from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

from .organizacion_modelo import Organizacion


class EventoBase(SQLModel):
    nombre: str
    precio_entrada: float
    disponible: bool = True
    descripcion: str
    fecha: datetime
    lugar: str
    organizacion_id: int | None = Field(default = None, foreign_key = "organizacion.id")


class Evento(EventoBase, table = True):
    id: int | None = Field(default = None, primary_key = True)
    organizacion: Organizacion | None = Relationship(back_populates = "evento")
    entradas_vendidas: int = 0


class EventoCreate(EventoBase):
    pass


class EventoPublic(EventoBase):
    id: int
    entradas_vendidas: int
