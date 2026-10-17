from .organizacion_modelo import OrganizacionPublic
from .evento_modelo import EventoPublic
from .usuario_modelo import UsuarioPublic


class EventoNested(EventoPublic):
    organizacion: OrganizacionPublic | None = None


class OrganizacionNested(OrganizacionPublic):
    evento: list[EventoPublic] | None = []


class UsuarioNested(UsuarioPublic):
    organizacion: list[OrganizacionPublic] | None = []
