from sqlalchemy import Column, ForeignKey, Integer, String, Enum as PgEnum
from sqlalchemy.orm import relationship
from .auxiliar import RolEnum
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# --------------------------------------------------------
# Usuario con roles
# --------------------------------------------------------
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(80), unique=True, nullable=False)
    hash_contraseña = Column(String(128), nullable=False)
    rol = Column(PgEnum(RolEnum), default=RolEnum.ESTUDIANTE, nullable=False)

    id_estudiante = Column(Integer, ForeignKey('estudiante.id'), nullable=True)
    id_profesor = Column(Integer, ForeignKey('profesor.id'), nullable=True)
    id_administrador = Column(Integer, ForeignKey('administrador.id'), nullable=True)
    id_jefe_departamento = Column(Integer, ForeignKey('jefe_departamento.id'), nullable=True)

    estudiante = relationship("Estudiante", back_populates="usuario", uselist=False)
    profesor = relationship("Profesor", back_populates="usuario", uselist=False)
    administrador = relationship("Administrador", back_populates="usuario", uselist=False)
    jefe_departamento = relationship("JefeDepartamento", back_populates="usuario", uselist=False)

    actividades_creadas = relationship("Actividad", back_populates="creador", cascade="all, delete-orphan")
    comentarios = relationship("Comentario", back_populates="autor", cascade="all, delete-orphan")

    def establecer_contraseña(self, contraseña):
        self.hash_contraseña = generate_password_hash(contraseña)

    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.hash_contraseña, contraseña)
    