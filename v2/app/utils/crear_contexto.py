# importa modelos
from ..models.actividad import Actividad  
from ..models.comentario import Comentario
from ..models.facultad import Facultad
from ..models.usuario import Usuario
from ..models.roles import *
from ..models.encuesta import *
from ..models.auxiliar import *

from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError

def crear_contexto(app):
    with app.app_context():
        from app.extensions import db
        db.create_all()
        
        try:
            # Verificar si ya existe el administrador
            admin_existente = Usuario.query.filter_by(rol=RolEnum.ADMINISTRADOR).first()

            
            if not admin_existente:
                admin_administrador = Administrador()
                admin_usuario = Usuario(
                    usuario='admin',
                    nombre_completo='Administrador por defecto',
                    correo='admin@admin.com',
                    rol=RolEnum.ADMINISTRADOR,
                    administrador=admin_administrador
                )
                admin_usuario.clave = generate_password_hash('123456')
                db.session.add(admin_administrador)
                db.session.add(admin_usuario)
                db.session.commit()
                print("Administrador por defecto creado correctamente.")
            else:
                print("El administrador por defecto ya existe.")
        except SQLAlchemyError as e:
            print("Error al crear el administrador por defecto:", str(e))
            db.session.rollback()
        except Exception as ex:
            print("Error inesperado:", str(ex))
            db.session.rollback()
            