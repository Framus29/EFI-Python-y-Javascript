from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ..database import get_db

from ..models import organizacion, anidados
from ..schemas.esquemas import PARAMETROS_ID


router = APIRouter(prefix = "/organizaciones", tags = ["organizaciones"])


@router.get("/", response_model = list[anidados.OrganizacionNested])
def mostrar_database_organizacion(db: Session = Depends(get_db)):
    return db.exec(select(organizacion.Organizacion)).all()


@router.get("/{id}", response_model = anidados.OrganizacionNested)
def mostrar_organizacion(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    organizacion_buscado = db.exec(select(organizacion.Organizacion).where(organizacion.Organizacion.id == id)).first()

    if organizacion_buscado is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con el de ningun organizacion")

    return organizacion_buscado


@router.post("/", response_model = organizacion.OrganizacionCreate)
def crear_organizacion(nuevo_organizacion: organizacion.OrganizacionCreate, db: Session = Depends(get_db)):

    if db.exec(select(organizacion.Organizacion).where(organizacion.Organizacion.nombre == nuevo_organizacion.nombre)).first():
        raise HTTPException(status_code = 400, detail = "el nombre del organizacion ya existe")

    db_organizacion = organizacion.Organizacion.model_validate(nuevo_organizacion)
    db.add(db_organizacion)
    db.commit()
    db.refresh(db_organizacion)

    return db_organizacion


@router.put("/{id}", response_model = organizacion.Organizacion)
def actualizar_organizacion(id: PARAMETROS_ID, organizacion_actualizado: organizacion.OrganizacionCreate, db: Session = Depends(get_db)):

    organizacion = db.exec(select(organizacion.Organizacion).where(organizacion.Organizacion.id == id)).first()

    if not organizacion:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun organizacion")

    organizacion.nombre = organizacion_actualizado.nombre
    organizacion.precio = organizacion_actualizado.precio
    organizacion.disponible = organizacion_actualizado.disponible
    organizacion.marca = organizacion_actualizado.marca

    db.commit()
    db.refresh(organizacion)

    return organizacion


@router.delete("/{id}", response_model = organizacion.OrganizacionPublic)
def borrar_organizacion(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    organizacion = db.exec(select(organizacion.Organizacion).where(organizacion.Organizacion.id == id)).first()

    if organizacion is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun organizacion")

    db.delete(organizacion)
    db.commit()

    return organizacion