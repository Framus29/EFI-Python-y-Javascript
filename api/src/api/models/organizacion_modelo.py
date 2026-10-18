from sqlmodel import Field, Relationship, SQLModel

from ..schemas.esquemas import PARAMETROS_NOMBRE


class OrganizacionBase(SQLModel):
    nombre: PARAMETROS_NOMBRE


class Organizacion(OrganizacionBase, table = True):
    id: int | None = Field(default = None, primary_key = True)
    evento: list["Evento"] | None = Relationship(back_populates = "organizacion")
    suscripcion: list["Suscripcion"] | None = Relationship(back_populates = "organizacion")


class OrganizacionCreate(OrganizacionBase):
    pass


class OrganizacionPublic(OrganizacionBase):
    id: int
