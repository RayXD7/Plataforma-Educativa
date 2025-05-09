import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.extensions import db


# --------------------------------------------------------
# Encuestas
# --------------------------------------------------------
class Encuesta(db.Model):
    __tablename__ = 'encuesta'
    id            = Column(Integer, primary_key=True)
    titulo        = Column(String(255), nullable=False)
    descripcion   = Column(String(255))
    editable      = Column(Boolean, default=False)  # si un profesor puede editar
    # Crear campo para la lista de opciones de la encuesta y que no sea obligatorio
    # opciones      = Column(String(255))  # Opciones de la encuesta
    
    creado_en     = Column(DateTime, default=db.func.current_timestamp())
    respuestas = relationship("Respuesta", back_populates="encuesta", cascade="all, delete-orphan")

class Respuesta(db.Model):
    __tablename__ = 'respuesta'
    id            = Column(Integer, primary_key=True)
    usuario_id    = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    encuesta_id   = Column(Integer, ForeignKey('encuesta.id'), nullable=False)
    respondido_en = Column(DateTime, default=db.func.current_timestamp())
    # opcion_id     = Column(Integer, ForeignKey('opcion.id'), nullable=False)
    usuario       = relationship("Usuario", back_populates="respuestas")
    encuesta      = relationship("Encuesta", back_populates="respuestas")
    # opcion        = relationship("Opcion", back_populates="respuestas")