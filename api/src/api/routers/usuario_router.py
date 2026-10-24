from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ..database import get_db
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

from ..models import usuario_modelo, anidados, suscripcion_modelo
from ..schemas.esquemas import PARAMETROS_ID


router = APIRouter(
    prefix = "/usuarios",
    tags = ["usuarios"]
    )


@router.get("/", response_model = Page[usuario_modelo.UsuarioPublic])
def mostrar_database_usuario(
    db: Session = Depends(get_db),
    ):

    query = select(usuario_modelo.Usuario)

    return paginate(db, query)


@router.get("/{id}", response_model = anidados.UsuarioNested)
def mostrar_usuario(
    id: PARAMETROS_ID,
    db: Session = Depends(get_db)
    ):

    usuario_buscado = db.exec(select(usuario_modelo.Usuario).where(usuario_modelo.Usuario.id == id)).first()

    if usuario_buscado is None:
        raise HTTPException(
            status_code = 404,
            detail = "el id no coincide con ningun usuario"
            )

    return usuario_buscado


@router.post("/", response_model = usuario_modelo.UsuarioPublic)
def crear_usuario(
    nuevo_usuario: usuario_modelo.UsuarioCreate,
    db: Session = Depends(get_db)
    ):

    if db.exec(select(usuario_modelo.Usuario).where(usuario_modelo.Usuario.nombre == nuevo_usuario.nombre)).first():
        raise HTTPException(
            status_code = 400,
            detail = "el nombre de usuario ya esta en uso"
            )

    if db.exec(select(usuario_modelo.Usuario).where(usuario_modelo.Usuario.email == nuevo_usuario.email)).first():
        raise HTTPException(
            status_code = 400,
            detail = "el email ya esta en uso"
            )

    db_usuario = usuario_modelo.Usuario.model_validate(nuevo_usuario)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    return db_usuario


@router.put("/{id}", response_model = usuario_modelo.UsuarioPublic)
def actualizar_usuario(
    id: PARAMETROS_ID,
    usuario_actualizado: usuario_modelo.UsuarioCreate,
    db: Session = Depends(get_db)
    ):

    usuario = db.exec(select(usuario_modelo.Usuario).where(usuario_modelo.Usuario.id == id)).first()

    if not usuario:
        raise HTTPException(
            status_code = 404,
            detail = "el id no coincide con ningun usuario"
            )
    
    if db.exec(select(usuario_modelo.Usuario).where(usuario_modelo.Usuario.nombre == usuario_actualizado.nombre, usuario_modelo.Usuario.id != id)).first():
        raise HTTPException(
            status_code = 400,
            detail = "el nombre de usuario ya esta en uso"
            )
    
    if db.exec(select(usuario_modelo.Usuario).where(usuario_modelo.Usuario.email == usuario_actualizado.email, usuario_modelo.Usuario.id != id)).first():
        raise HTTPException(
            status_code = 400,
            detail = "el email ya esta en uso"
            )

    usuario.nombre = usuario_actualizado.nombre
    usuario.email = usuario_actualizado.email
    usuario.fecha_nacimiento = usuario_actualizado.fecha_nacimiento
    usuario.contrasenia = usuario_actualizado.contrasenia

    db.commit()
    db.refresh(usuario)

    return usuario


@router.delete("/{id}", response_model = usuario_modelo.UsuarioPublic)
def borrar_usuario(
    id: PARAMETROS_ID,
    db: Session = Depends(get_db)
    ):

    usuario = db.exec(select(usuario_modelo.Usuario).where(usuario_modelo.Usuario.id == id)).first()
    suscripciones_del_usuario = db.exec(select(suscripcion_modelo.Suscripcion).where(suscripcion_modelo.Suscripcion.usuario_id == id))

    if usuario is None:
        raise HTTPException(
            status_code = 404,
            detail = "el id no coincide con ningun usuario"
            )

    for suscripcion in suscripciones_del_usuario:
        db.delete(suscripcion)

    db.delete(usuario)    
    db.commit()

    return usuario
