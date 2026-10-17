from sqlmodel import Field, Relationship, SQLModel

from ..schemas.esquemas import PARAMETROS_NOMBRE


class OrganizacionBase(SQLModel):
    nombre: str = PARAMETROS_NOMBRE


class Organizacion(OrganizacionBase, table = True):
    id: int | None = Field(default = None, primary_key = True)
    evento: list["Evento"] | None = Relationship(back_populates = "organizacion")
    usuario: list["Usuario"] | None = Relationship(back_populates = "organizacion")


class OrganizacionCreate(OrganizacionBase):
    pass


class OrganizacionPublic(OrganizacionBase):
    id: int
