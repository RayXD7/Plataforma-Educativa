from flask import Flask

def registrar_rutas(app:Flask):
    from .main import main_bp
    app.register_blueprint(main_bp)
    
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from .teacher import teacher_bp
    app.register_blueprint(teacher_bp)
    
    from .student import student_bp
    app.register_blueprint(student_bp)
    
    from .jefe_d import jefe_bp
    app.register_blueprint(jefe_bp)