from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ..database import get_db

from ..models import usuario, anidados
from ..schemas.esquemas import PARAMETROS_ID


router = APIRouter(prefix = "/usuarios", tags = ["usuarios"])


@router.get("/", response_model = list[anidados.UsuarioNested])
def mostrar_database_usuario(db: Session = Depends(get_db)):
    return db.exec(select(usuario.Usuario)).all()


@router.get("/{id}", response_model = anidados.UsuarioNested)
def mostrar_usuario(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    usuario_buscado = db.exec(select(usuario.Usuario).where(usuario.Usuario.id == id)).first()

    if usuario_buscado is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con el de ningun usuario")

    return usuario_buscado


@router.post("/", response_model = usuario.UsuarioCreate)
def crear_usuario(nuevo_usuario: usuario.UsuarioCreate, db: Session = Depends(get_db)):

    if db.exec(select(usuario.Usuario).where(usuario.Usuario.nombre == nuevo_usuario.nombre)).first():
        raise HTTPException(status_code = 400, detail = "el nombre del usuario ya existe")

    db_usuario = usuario.Usuario.model_validate(nuevo_usuario)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    return db_usuario


@router.put("/{id}", response_model = usuario.Usuario)
def actualizar_usuario(id: PARAMETROS_ID, usuario_actualizado: usuario.UsuarioCreate, db: Session = Depends(get_db)):

    usuario = db.exec(select(usuario.Usuario).where(usuario.Usuario.id == id)).first()

    if not usuario:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun usuario")

    usuario.nombre = usuario_actualizado.nombre
    usuario.precio = usuario_actualizado.precio
    usuario.disponible = usuario_actualizado.disponible
    usuario.marca = usuario_actualizado.marca

    db.commit()
    db.refresh(usuario)

    return usuario


@router.delete("/{id}", response_model = usuario.UsuarioPublic)
def borrar_usuario(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    usuario = db.exec(select(usuario.Usuario).where(usuario.Usuario.id == id)).first()

    if usuario is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun usuario")

    db.delete(usuario)
    db.commit()

    return usuario