# SQLAlchemy models here
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)

    usuarios = relationship("Usuario", back_populates="rol")


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    contrasena = Column(String, nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"))

    rol = relationship("Rol", back_populates="usuarios")
    empleado = relationship("Empleado", back_populates="usuario", uselist=False)


class Empleado(Base):
    __tablename__ = "empleados"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    nombres = Column(String)
    apellidos = Column(String)
    telefono = Column(String)
    direccion = Column(String)
    emergencia_nombre = Column(String)
    emergencia_telefono = Column(String)
    departamento = Column(String)
    cargo = Column(String)
    fecha_ingreso = Column(Date)

    usuario = relationship("Usuario", back_populates="empleado")
    asistencias = relationship("Asistencia", back_populates="empleado")
    evaluaciones = relationship("Evaluacion", back_populates="empleado")


class Documento(Base):
    __tablename__ = "documentos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    categoria = Column(String)
    ruta = Column(String)
    creado_por = Column(Integer, ForeignKey("usuarios.id"))
    fecha_subido = Column(DateTime, default=datetime.datetime.utcnow)


class Solicitud(Base):
    __tablename__ = "solicitudes"
    id = Column(Integer, primary_key=True)
    tipo = Column(String)  # 'vacante', 'permiso', etc.
    descripcion = Column(Text)
    creado_por = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(DateTime, default=datetime.datetime.utcnow)


class Asistencia(Base):
    __tablename__ = "asistencias"
    id = Column(Integer, primary_key=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"))
    fecha = Column(Date, default=datetime.date.today)
    entrada = Column(String)
    salida = Column(String)

    empleado = relationship("Empleado", back_populates="asistencias")


class Evaluacion(Base):
    __tablename__ = "evaluaciones"
    id = Column(Integer, primary_key=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"))
    tipo = Column(String)  # 'auto', 'pares', 'gerente'
    puntaje = Column(Float)
    comentarios = Column(Text)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)

    empleado = relationship("Empleado", back_populates="evaluaciones")
