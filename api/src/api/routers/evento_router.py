from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

from ..database import get_db
from ..models import evento_modelo, anidados, organizacion_modelo
from ..schemas.esquemas import PARAMETROS_ID, not_found


router = APIRouter(
    prefix = "/eventos",
    tags = ["eventos"]
    )


@router.get("/", response_model = Page[anidados.EventoPublic])
def mostrar_database_evento(
    db: Session = Depends(get_db),
    ):

    query = select(evento_modelo.Evento)

    return paginate(db, query)


@router.get("/{id}", response_model = anidados.EventoNested, responses = not_found)
def mostrar_evento(
    id: PARAMETROS_ID,
    db: Session = Depends(get_db)
    ):

    evento_buscado = db.exec(select(evento_modelo.Evento).where(evento_modelo.Evento.id == id)).first()

    if evento_buscado is None:
        raise HTTPException(
            status_code = 404,
            detail = "el id no coincide con ningun evento"
            )

    return evento_buscado


@router.post("/", response_model = evento_modelo.EventoPublic, responses = not_found)
def crear_evento(
    nuevo_evento: evento_modelo.EventoCreate,
    db: Session = Depends(get_db)
    ):

    db_evento = evento_modelo.Evento.model_validate(nuevo_evento)

    if not db.exec(select(organizacion_modelo.Organizacion).where(organizacion_modelo.Organizacion.id == nuevo_evento.organizacion_id)).first():
        raise HTTPException(
            status_code = 400,
            detail = "la organizacion no existe"
            )

    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)

    return db_evento


@router.put("/{id}", response_model = evento_modelo.EventoPublic, responses = not_found)
def actualizar_evento(
    id: PARAMETROS_ID,
    evento_actualizado: evento_modelo.EventoCreate,
    db: Session = Depends(get_db)
    ):

    evento = db.exec(select(evento_modelo.Evento).where(evento_modelo.Evento.id == id)).first()

    if not evento:
        raise HTTPException(
            status_code = 404,
            detail = "el id no coincide con ningun evento"
            )

    if not db.exec(select(organizacion_modelo.Organizacion).where(organizacion_modelo.Organizacion.id == evento_actualizado.organizacion_id)).first():
        raise HTTPException(
            status_code = 400,
            detail = "la organizacion no existe"
            )

    evento.nombre = evento_actualizado.nombre
    evento.precio_entrada = evento_actualizado.precio_entrada
    evento.disponible = evento_actualizado.disponible
    evento.descripcion = evento_actualizado.descripcion
    evento.fecha = evento_actualizado.fecha
    evento.lugar = evento_actualizado.lugar
    evento.organizacion_id = evento_actualizado.organizacion_id

    db.commit()
    db.refresh(evento)

    return evento


@router.delete("/{id}", response_model = evento_modelo.EventoPubli, responses = not_found)
def borrar_evento(
    id: PARAMETROS_ID,
    db: Session = Depends(get_db)
    ):

    evento = db.exec(select(evento_modelo.Evento).where(evento_modelo.Evento.id == id)).first()

    if evento is None:
        raise HTTPException(
            status_code = 404,
            detail = "el id no coincide con ningun evento"
            )

    db.delete(evento)
    db.commit()

    return evento
