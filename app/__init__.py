from flask import Flask
from .config import ConfiguracionDespliegue, ConfiguracionDesarrollo

def crear_app(config=ConfiguracionDesarrollo):
    app = Flask(__name__)
    app.config.from_object(config)
    
    from .extensions import iniciar_extensiones
    iniciar_extensiones(app)
    
    from .utils.crear_contexto import crear_contexto
    crear_contexto(app)
    
    from .routes import registrar_rutas
    registrar_rutas(app)
    
    return app

if __name__ == "__main__":
    crear_app()