from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

from ..models import suscripcion_modelo, anidados, usuario_modelo, organizacion_modelo
from ..schemas.esquemas import PARAMETROS_ID, not_found


router = APIRouter(prefix = "/suscripciones", tags = ["suscripciones"])


@router.get("/", response_model = Page[anidados.SuscripcionPublic])
def mostrar_database_suscripcion(
    db: Session = Depends(get_db),
    ):

    query = select(suscripcion_modelo.Suscripcion)

    return paginate(db, query)


@router.get("/{id}", response_model = anidados.SuscripcionNested, responses = not_found)
def mostrar_suscripcion(
    id: PARAMETROS_ID,
    db: Session = Depends(get_db)
    ):

    suscripcion_buscado = db.exec(select(suscripcion_modelo.Suscripcion).where(suscripcion_modelo.Suscripcion.id == id)).first()

    if suscripcion_buscado is None:
        raise HTTPException(
            status_code = 404,
            detail = "el id no coincide con ninguna suscripcion"
            )

    return suscripcion_buscado


@router.post("/", response_model = suscripcion_modelo.SuscripcionPublic, responses = not_found)
def crear_suscripcion(nueva_suscripcion: suscripcion_modelo.SuscripcionCreate, db: Session = Depends(get_db)):

    if not db.exec(select(usuario_modelo.Usuario).where(usuario_modelo.Usuario.id == nueva_suscripcion.usuario_id)).first():
        raise HTTPException(
            status_code = 400,
            detail = "ese id de usuario no existe"
            )

    if not db.exec(select(organizacion_modelo.Organizacion).where(organizacion_modelo.Organizacion.id == nueva_suscripcion.organizacion_id)).first():
        raise HTTPException(
            status_code = 400,
            detail = "ese id de organizacion no existe"
            )

    db_suscripcion = suscripcion_modelo.Suscripcion.model_validate(nueva_suscripcion)

    try:
        db.add(db_suscripcion)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code = 409,
            detail = "la suscripcion ya estaba hecha"
            )

    db.refresh(db_suscripcion)

    return db_suscripcion


@router.delete("/{id}", response_model = suscripcion_modelo.SuscripcionPublic, responses = not_found)
def borrar_suscripcion(
    id: PARAMETROS_ID,
    db: Session = Depends(get_db)
    ):

    suscripcion = db.exec(select(suscripcion_modelo.Suscripcion).where(suscripcion_modelo.Suscripcion.id == id)).first()

    if suscripcion is None:
        raise HTTPException(
            status_code = 404,
            detail = "el id no coincide con ninguna suscripcion"
            )

    db.delete(suscripcion)
    db.commit()

    return suscripcion
