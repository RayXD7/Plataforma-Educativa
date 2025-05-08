from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.extensions import db
import datetime

# --------------------------------------------------------
# Comentarios sobre actividades
# --------------------------------------------------------
class Comentario(db.Model):
    __tablename__ = 'comentario'
    id          = Column(Integer, primary_key=True, autoincrement=True)
    contenido   = Column(Text, nullable=False)
    creado_en   = Column(DateTime, default=datetime.timezone.utc, nullable=False)
    autor_id    = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)
    autor       = relationship("Usuario", back_populates="comentarios")
    actividad   = relationship("Actividad", back_populates="comentarios")