from flask import Flask

def registrar_rutas(app:Flask):
    from .main import main_bp
    app.register_blueprint(main_bp)
    
    from .auth import auth_bp
    app.register_blueprint(auth_bp)