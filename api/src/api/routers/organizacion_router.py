from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ..database import get_db
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

from ..models import organizacion_modelo, anidados, evento_modelo, suscripcion_modelo
from ..schemas.esquemas import PARAMETROS_ID, not_found


router = APIRouter(
    prefix = "/organizaciones",
    tags = ["organizaciones"]
    )


@router.get("/", response_model = Page[anidados.OrganizacionPublic])
def mostrar_database_organizacion(
    db: Session = Depends(get_db),
    ):

    query = select(organizacion_modelo.Organizacion)

    return paginate(db, query)


@router.get("/{id}", response_model = anidados.OrganizacionNested, responses = not_found)
def mostrar_organizacion(
    id: PARAMETROS_ID,
    db: Session = Depends(get_db)
    ):

    organizacion_buscado = db.exec(select(organizacion_modelo.Organizacion).where(organizacion_modelo.Organizacion.id == id)).first()

    if organizacion_buscado is None:
        raise HTTPException(
            status_code = 404,
            detail = "el id no coincide con ninguna organizacion"
            )

    return organizacion_buscado


@router.post("/", response_model = organizacion_modelo.OrganizacionPublic, responses = not_found)
def crear_organizacion(
    nuevo_organizacion: organizacion_modelo.OrganizacionCreate,
    db: Session = Depends(get_db)
    ):

    db_organizacion = organizacion_modelo.Organizacion.model_validate(nuevo_organizacion)
    
    if db.exec(select(organizacion_modelo.Organizacion).where(organizacion_modelo.Organizacion.nombre == nuevo_organizacion.nombre)).first():
        raise HTTPException(
            status_code = 400,
            detail = "el nombre de la organizacion ya existe"
            )

    db.add(db_organizacion)
    db.commit()
    db.refresh(db_organizacion)

    return db_organizacion


@router.put("/{id}", response_model = organizacion_modelo.OrganizacionPublic, responses = not_found)
def actualizar_organizacion(
    id: PARAMETROS_ID,
    organizacion_actualizado: organizacion_modelo.OrganizacionCreate,
    db: Session = Depends(get_db)
    ):

    organizacion = db.exec(select(organizacion_modelo.Organizacion).where(organizacion_modelo.Organizacion.id == id)).first()

    if not organizacion:
        raise HTTPException(
            status_code = 404,
            detail = "el id no coincide con ninguna organizacion"
            )

    organizacion.nombre = organizacion_actualizado.nombre

    db.commit()
    db.refresh(organizacion)

    return organizacion


@router.delete("/{id}", response_model = organizacion_modelo.OrganizacionPublic, responses = not_found)
def borrar_organizacion(
    id: PARAMETROS_ID,
    db: Session = Depends(get_db)
    ):

    organizacion = db.exec(select(organizacion_modelo.Organizacion).where(organizacion_modelo.Organizacion.id == id)).first()
    eventos_de_la_organizacion = db.exec(select(evento_modelo.Evento).where(evento_modelo.Evento.organizacion_id == id))
    suscriptores_de_la_organizacion = db.exec(select(suscripcion_modelo.Suscripcion).where(suscripcion_modelo.Suscripcion.organizacion_id == id))

    if organizacion is None:
        raise HTTPException(
            status_code = 404,
            detail = "el id no coincide con ninguna organizacion"
            )

    for evento in eventos_de_la_organizacion:
        db.delete(evento)
    for suscripcion in suscriptores_de_la_organizacion:
        db.delete(suscripcion)

    db.delete(organizacion)
    db.commit()

    return organizacion
