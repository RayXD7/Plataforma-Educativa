from sqlalchemy import Boolean, Column, Integer, Text, String, DateTime, Enum as PgEnum, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from app.extensions import db
from .auxiliar import TipoActividadEnum, participantes_actividad

# --------------------------------------------------------
# Actividades
# --------------------------------------------------------
class Actividad(db.Model):
    __tablename__ = 'actividad'
    id          = Column(Integer, primary_key=True, autoincrement=True)
    titulo      = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha       = Column(DateTime, default=datetime.timezone.utc, nullable=False)
    enviada = Column(Boolean, default=False, nullable=False)
    tipo        = Column(PgEnum(TipoActividadEnum), default=TipoActividadEnum.NO_OFICIAL, nullable=False)
    # creador de la actividad
    creador_id  = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    creador     = relationship("Usuario", back_populates="actividades_creadas")
    # participantes y comentarios
    participantes = relationship(
        "Usuario",
        secondary=participantes_actividad,
        backref="actividades_participando"
    )
    comentarios   = relationship("Comentario", back_populates="actividad", cascade="all, delete-orphan")