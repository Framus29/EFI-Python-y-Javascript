from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import UniqueConstraint

from .organizacion_modelo import Organizacion
from .usuario_modelo import Usuario


class SuscripcionBase(SQLModel):
    usuario_id: int | None = Field(default = None, foreign_key = "usuario.id")
    organizacion_id: int | None = Field(default = None, foreign_key = "organizacion.id")


class Suscripcion(SuscripcionBase, table = True):
    __table_args__ = (UniqueConstraint("usuario_id", "organizacion_id"),) # segun la IA, con esto evito que un usuario se suscriba multiples veces a una misma organizacion
    id: int | None = Field(default = None, primary_key = True)
    usuario: Usuario | None = Relationship(back_populates = "suscripcion")
    organizacion: Organizacion | None = Relationship(back_populates = "suscripcion")


class SuscripcionCreate(SuscripcionBase):
    pass


class SuscripcionPublic(SuscripcionBase):
    id: int
