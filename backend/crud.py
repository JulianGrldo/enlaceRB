# backend/crud.py

from sqlalchemy.orm import Session
from . import models, schemas
import bcrypt
from typing import List, Optional
from datetime import date

# --- Helper para Contraseñas ---
def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# --- CRUD para Rol ---
def get_rol(db: Session, rol_id: int) -> Optional[models.Rol]:
    """Obtiene un rol por su ID."""
    return db.query(models.Rol).filter(models.Rol.id == rol_id).first()

def get_rol_by_nombre(db: Session, nombre: str) -> Optional[models.Rol]:
    """Obtiene un rol por su nombre."""
    return db.query(models.Rol).filter(models.Rol.nombre == nombre).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[models.Rol]:
    """Obtiene una lista de todos los roles."""
    return db.query(models.Rol).offset(skip).limit(limit).all()

def create_rol(db: Session, rol: schemas.RolCreate) -> models.Rol:
    """Crea un nuevo rol."""
    db_rol = models.Rol(nombre=rol.nombre)
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

# --- CRUD para Usuario ---
def get_usuario(db: Session, usuario_id: int) -> Optional[models.Usuario]:
    """Obtiene un usuario por su ID."""
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_usuario_by_correo(db: Session, correo: str) -> Optional[models.Usuario]:
    """Obtiene un usuario por su correo electrónico."""
    return db.query(models.Usuario).filter(models.Usuario.correo == correo).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> List[models.Usuario]:
    """Obtiene una lista de todos los usuarios."""
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate) -> models.Usuario:
    """Crea un nuevo usuario con contraseña hasheada."""
    hashed_password = hash_password(usuario.contrasena)
    db_usuario = models.Usuario(
        correo=usuario.correo,
        nombre=usuario.nombre,
        contrasena=hashed_password,
        rol_id=usuario.rol_id
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# --- CRUD para Empleado ---
def get_empleado(db: Session, empleado_id: int) -> Optional[models.Empleado]:
    """Obtiene un perfil de empleado por su ID."""
    return db.query(models.Empleado).filter(models.Empleado.id == empleado_id).first()

def get_empleados(db: Session, skip: int = 0, limit: int = 100) -> List[models.Empleado]:
    """Obtiene una lista de todos los empleados."""
    return db.query(models.Empleado).offset(skip).limit(limit).all()

def create_empleado(db: Session, empleado: schemas.EmpleadoCreate) -> models.Empleado:
    """Crea un nuevo perfil de empleado (generalmente al crear un usuario)."""
    db_empleado = models.Empleado(**empleado.dict())
    db.add(db_empleado)
    db.commit()
    db.refresh(db_empleado)
    return db_empleado

def update_empleado(db: Session, empleado_id: int, empleado_data: schemas.EmpleadoUpdate) -> Optional[models.Empleado]:
    """Actualiza la información de un perfil de empleado."""
    db_empleado = get_empleado(db, empleado_id)
    if db_empleado:
        # exclude_unset=True asegura que solo los campos proporcionados se actualicen
        update_data = empleado_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_empleado, key, value)
        db.commit()
        db.refresh(db_empleado)
    return db_empleado

# --- CRUD para Documento ---
def get_documento(db: Session, documento_id: int) -> Optional[models.Documento]:
    """Obtiene un documento por su ID."""
    return db.query(models.Documento).filter(models.Documento.id == documento_id).first()

def get_documentos(db: Session, skip: int = 0, limit: int = 100) -> List[models.Documento]:
    """Obtiene una lista de todos los documentos."""
    return db.query(models.Documento).order_by(models.Documento.fecha_subido.desc()).offset(skip).limit(limit).all()

def create_documento(db: Session, documento: schemas.DocumentoCreate) -> models.Documento:
    """Guarda la información de un nuevo documento en la base de datos."""
    db_documento = models.Documento(**documento.dict())
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

# --- CRUD para Solicitud ---
def get_solicitud(db: Session, solicitud_id: int) -> Optional[models.Solicitud]:
    """Obtiene una solicitud por su ID."""
    return db.query(models.Solicitud).filter(models.Solicitud.id == solicitud_id).first()

def get_solicitudes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Solicitud]:
    """Obtiene una lista de todas las solicitudes."""
    return db.query(models.Solicitud).order_by(models.Solicitud.fecha.desc()).offset(skip).limit(limit).all()

def create_solicitud(db: Session, solicitud: schemas.SolicitudCreate) -> models.Solicitud:
    """Crea una nueva solicitud (de vacante, permiso, etc.)."""
    db_solicitud = models.Solicitud(**solicitud.dict())
    db.add(db_solicitud)
    db.commit()
    db.refresh(db_solicitud)
    return db_solicitud

# --- CRUD para Asistencia ---
def get_asistencias_by_empleado(db: Session, empleado_id: int) -> List[models.Asistencia]:
    """Obtiene todos los registros de asistencia para un empleado."""
    return db.query(models.Asistencia).filter(models.Asistencia.empleado_id == empleado_id).all()

def get_asistencia_by_empleado_and_fecha(db: Session, empleado_id: int, fecha: date) -> Optional[models.Asistencia]:
    """Obtiene el registro de asistencia de un empleado para una fecha específica."""
    return db.query(models.Asistencia).filter(
        models.Asistencia.empleado_id == empleado_id,
        models.Asistencia.fecha == fecha
    ).first()

def create_or_update_asistencia(db: Session, asistencia_data: schemas.AsistenciaCreate) -> models.Asistencia:
    """Crea un nuevo registro de asistencia o actualiza la salida si ya existe la entrada."""
    db_asistencia = get_asistencia_by_empleado_and_fecha(db, asistencia_data.empleado_id, asistencia_data.fecha)
    if db_asistencia:
        # Actualiza la hora de salida
        db_asistencia.salida = asistencia_data.salida
    else:
        # Crea un nuevo registro
        db_asistencia = models.Asistencia(**asistencia_data.dict())
        db.add(db_asistencia)
    db.commit()
    db.refresh(db_asistencia)
    return db_asistencia

# --- CRUD para Evaluacion ---
def get_evaluacion(db: Session, evaluacion_id: int) -> Optional[models.Evaluacion]:
    """Obtiene una evaluación por su ID."""
    return db.query(models.Evaluacion).filter(models.Evaluacion.id == evaluacion_id).first()

def get_evaluaciones_by_empleado(db: Session, empleado_id: int) -> List[models.Evaluacion]:
    """Obtiene todas las evaluaciones de un empleado."""
    return db.query(models.Evaluacion).filter(models.Evaluacion.empleado_id == empleado_id).all()

def create_evaluacion(db: Session, evaluacion: schemas.EvaluacionCreate) -> models.Evaluacion:
    """Crea un nuevo registro de evaluación de desempeño."""
    db_evaluacion = models.Evaluacion(**evaluacion.dict())
    db.add(db_evaluacion)
    db.commit()
    db.refresh(db_evaluacion)
    return db_evaluacion