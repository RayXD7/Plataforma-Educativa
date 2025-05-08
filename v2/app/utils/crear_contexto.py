# importa modelos
from ..models.actividad import Actividad  
from ..models.comentario import Comentario
from ..models.facultad import Facultad
from ..models.usuario import Usuario
from ..models.encuesta import *
from ..models.auxiliar import *

def crear_contexto(app):
    
    with app.app_context():
        from ..extensions import db
        db.create_all()