from .organizacion_modelo import OrganizacionPublic
from .evento_modelo import EventoPublic
from .usuario_modelo import UsuarioPublic
from .suscripcion_modelo import SuscripcionPublic


class EventoNested(EventoPublic):
    organizacion: OrganizacionPublic | None = None

class OrganizacionNested(OrganizacionPublic):
    evento: list[EventoPublic] | None = []


class SuscripcionNested(SuscripcionPublic):
    organizacion: OrganizacionPublic | None = None

class UsuarioNested(UsuarioPublic):
    suscripcion: list[SuscripcionNested] | None = []
