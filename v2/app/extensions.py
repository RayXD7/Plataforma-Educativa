from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
db=SQLAlchemy()
migrate=Migrate()
login_manager=LoginManager()

def iniciar_extensiones(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)