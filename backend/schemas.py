# backend/schemas.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

# --- Esquemas para Rol ---
class RolBase(BaseModel):
    nombre: str

class RolCreate(RolBase):
    pass

class Rol(RolBase):
    id: int

    class Config:
        orm_mode = True

# --- Esquemas para Usuario ---
class UsuarioBase(BaseModel):
    nombre: str
    correo: str

class UsuarioCreate(UsuarioBase):
    contrasena: str
    rol_id: int

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    rol_id: Optional[int] = None

class Usuario(UsuarioBase):
    id: int
    rol: Rol

    class Config:
        orm_mode = True

# --- Esquemas para Empleado ---
class EmpleadoBase(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    emergencia_nombre: Optional[str] = None
    emergencia_telefono: Optional[str] = None
    departamento: Optional[str] = None
    cargo: Optional[str] = None
    fecha_ingreso: Optional[date] = None

class EmpleadoCreate(EmpleadoBase):
    usuario_id: int

class EmpleadoUpdate(EmpleadoBase):
    pass

class Empleado(EmpleadoBase):
    id: int
    usuario: Usuario  # Anidamos el esquema de Usuario para obtener sus datos

    class Config:
        orm_mode = True

# --- Esquemas para Documento ---
class DocumentoBase(BaseModel):
    nombre: str
    categoria: str
    ruta: str

class DocumentoCreate(DocumentoBase):
    creado_por: int

class Documento(DocumentoBase):
    id: int
    fecha_subido: datetime

    class Config:
        orm_mode = True

# --- Esquemas para Solicitud ---
class SolicitudBase(BaseModel):
    tipo: str
    descripcion: str

class SolicitudCreate(SolicitudBase):
    creado_por: int

class Solicitud(SolicitudBase):
    id: int
    fecha: datetime

    class Config:
        orm_mode = True

# --- Esquemas para Asistencia ---
class AsistenciaBase(BaseModel):
    fecha: date
    entrada: Optional[str] = None
    salida: Optional[str] = None

class AsistenciaCreate(AsistenciaBase):
    empleado_id: int

class Asistencia(AsistenciaBase):
    id: int

    class Config:
        orm_mode = True

# --- Esquemas para Evaluacion ---
class EvaluacionBase(BaseModel):
    tipo: str # 'auto', 'pares', 'gerente'
    puntaje: float
    comentarios: Optional[str] = None

class EvaluacionCreate(EvaluacionBase):
    empleado_id: int

class Evaluacion(EvaluacionBase):
    id: int
    fecha: datetime

    class Config:
        orm_mode = True