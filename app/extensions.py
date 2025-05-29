from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect

csrf = CSRFProtect()  # Protege toda la app
db=SQLAlchemy()
migrate=Migrate()
login_manager=LoginManager()

def iniciar_extensiones(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

from app.models.usuario import Usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))