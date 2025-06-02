from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.extensions import db

# --------------------------------------------------------
# Facultad
# --------------------------------------------------------
class Facultad(db.Model):
    __tablename__ = 'facultad'
    id     = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    carrera = relationship()

class Carrera(db.Model):
    id     = Column(Integer, primary_key=True, autoincrement=True)
    nombre  = Column(String(100), unique=True, nullable=False)

    profesores = relationship(
        "Usuario", back_populates="facultad",
        primaryjoin="and_(Usuario.facultad_id==Facultad.id, Usuario.rol=='profesor')",
        overlaps="estudiantes,jefe_departamento"
    )
    estudiantes = relationship(
        "Usuario", back_populates="facultad",
        primaryjoin="and_(Usuario.facultad_id==Facultad.id, Usuario.rol=='estudiante')",
        overlaps="profesores,jefe_departamento"
    )
    jefe_departamento = relationship(
        "Usuario", back_populates="facultad",
        primaryjoin="and_(Usuario.facultad_id==Facultad.id, Usuario.rol=='jefe_departamento')",
        overlaps="profesores,estudiantes"
    )
