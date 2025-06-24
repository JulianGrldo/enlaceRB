# backend/main.py

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine

# Crea las tablas en la base de datos (si no existen) al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EnlaceRB API",
    description="La API para la intranet corporativa EnlaceRB.",
    version="1.0.0"
)

# --- Dependencia para la Sesión de DB ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Router para Autenticación y Usuarios/Roles ---
api_router = APIRouter()

@api_router.post("/roles/", response_model=schemas.Rol, tags=["Roles"])
def create_rol(rol: schemas.RolCreate, db: Session = Depends(get_db)):
    db_rol = crud.get_rol_by_nombre(db, nombre=rol.nombre)
    if db_rol:
        raise HTTPException(status_code=400, detail="El rol ya existe")
    return crud.create_rol(db=db, rol=rol)

@api_router.get("/roles/", response_model=List[schemas.Rol], tags=["Roles"])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_roles(db, skip=skip, limit=limit)

@api_router.post("/usuarios/", response_model=schemas.Usuario, tags=["Usuarios"])
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_by_correo(db, correo=usuario.correo)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    # Al crear un usuario, podrías crear automáticamente su perfil de empleado vacío
    new_user = crud.create_usuario(db=db, usuario=usuario)
    empleado_data = schemas.EmpleadoCreate(usuario_id=new_user.id)
    crud.create_empleado(db=db, empleado=empleado_data)
    return new_user

@api_router.get("/usuarios/", response_model=List[schemas.Usuario], tags=["Usuarios"])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_usuarios(db, skip=skip, limit=limit)

@api_router.get("/usuarios/{usuario_id}", response_model=schemas.Usuario, tags=["Usuarios"])
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# --- Router para Empleados ---
@api_router.get("/empleados/", response_model=List[schemas.Empleado], tags=["Empleados"])
def read_empleados(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_empleados(db, skip=skip, limit=limit)

@api_router.get("/empleados/{empleado_id}", response_model=schemas.Empleado, tags=["Empleados"])
def read_empleado(empleado_id: int, db: Session = Depends(get_db)):
    db_empleado = crud.get_empleado(db, empleado_id=empleado_id)
    if db_empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return db_empleado

@api_router.put("/empleados/{empleado_id}", response_model=schemas.Empleado, tags=["Empleados"])
def update_empleado(empleado_id: int, empleado: schemas.EmpleadoUpdate, db: Session = Depends(get_db)):
    db_empleado = crud.update_empleado(db, empleado_id=empleado_id, empleado_data=empleado)
    if db_empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado para actualizar")
    return db_empleado

# --- Incluir el router en la aplicación principal ---
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def home():
    return {"mensaje": "Bienvenido al backend de EnlaceRB. Ve a /docs para la documentación de la API."}