from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ..database import get_db

from ..models import evento_modelo, anidados
from ..schemas.esquemas import PARAMETROS_ID


router = APIRouter(prefix = "/eventos", tags = ["eventos"])


@router.get("/", response_model = list[anidados.EventoNested])
def mostrar_database_evento(db: Session = Depends(get_db)):
    return db.exec(select(evento_modelo.Evento)).all()


@router.get("/{id}", response_model = anidados.EventoNested)
def mostrar_evento(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    evento_buscado = db.exec(select(evento_modelo.Evento).where(evento_modelo.Evento.id == id)).first()

    if evento_buscado is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con el de ningun evento")

    return evento_buscado


@router.post("/", response_model = evento_modelo.EventoCreate)
def crear_evento(nuevo_evento: evento_modelo.EventoCreate, db: Session = Depends(get_db)):

    if db.exec(select(evento_modelo.Evento).where(evento_modelo.Evento.nombre == nuevo_evento.nombre)).first():
        raise HTTPException(status_code = 400, detail = "el nombre del evento ya existe")

    db_evento = evento_modelo.Evento.model_validate(nuevo_evento)

    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)

    return db_evento


@router.put("/{id}", response_model = evento_modelo.Evento)
def actualizar_evento(id: PARAMETROS_ID, evento_actualizado: evento_modelo.EventoCreate, db: Session = Depends(get_db)):

    evento = db.exec(select(evento_modelo.Evento).where(evento_modelo.Evento.id == id)).first()

    if not evento:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun evento")

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


@router.delete("/{id}", response_model = evento_modelo.EventoPublic)
def borrar_evento(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    evento = db.exec(select(evento_modelo.Evento).where(evento_modelo.Evento.id == id)).first()

    if evento is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun evento")

    db.delete(evento)
    db.commit()

    return evento