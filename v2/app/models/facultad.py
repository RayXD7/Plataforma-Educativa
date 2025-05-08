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
    # relacion entre profesores y estudiantes que pertenecen a esta facultad
    
    profesores = relationship("Usuario", back_populates="facultad", 
                              primaryjoin="and_(Usuario.facultad_id==Facultad.id, Usuario.rol=='profesor')")
    estudiantes = relationship("Usuario", back_populates="facultad", 
                               primaryjoin="and_(Usuario.facultad_id==Facultad.id, Usuario.rol=='estudiante')")
    jefe_departamento = relationship("Usuario", back_populates="facultad",
                                 primaryjoin="and_(Usuario.facultad_id==Facultad.id, Usuario.rol=='jefe_departamento')")