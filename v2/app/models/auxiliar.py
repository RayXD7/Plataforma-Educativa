from sqlalchemy import Table, Integer, Column, DateTime, ForeignKey
from app.extensions import db
from enum import Enum
import datetime

# --------------------------------------------------------
# Tablas auxiliares y enums
# --------------------------------------------------------
class RolEnum(str, Enum):
    ADMINISTRADOR = "administrador"
    PROFESOR      = "profesor"
    ESTUDIANTE    = "estudiante"
    JEFE_DEPARTAMENTO = 'jefe_departamento'
    
class TipoActividadEnum(str, Enum):
    OFICIAL    = "oficial"
    NO_OFICIAL = "no_oficial"
    
# Tabla mucho-a-mucho para participantes de actividad
participantes_actividad = Table(
    'participantes_actividad',
    db.Model.metadata,
    Column('actividad_id', Integer, ForeignKey('actividad.id'), primary_key=True),
    Column('usuario_id', Integer, ForeignKey('usuario.id'), primary_key=True),
    Column('unido_en', DateTime, default=datetime.timezone.utc)
)