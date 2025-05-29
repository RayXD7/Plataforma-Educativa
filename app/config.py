from dotenv import load_dotenv
import os
load_dotenv()

class ConfiguracionBasica:
    """Clase de configuración básica."""
    TOKEN_ACCESO = os.getenv('TOKEN_ACCESO')
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-secreta-por-defecto')  # Mejor usar en producción
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ConfiguracionDesarrollo(ConfiguracionBasica):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///desarrollo.db'

class ConfiguracionDespliegue(ConfiguracionBasica):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

if __name__ == "__main__":
    print("DB URI:", os.getenv('SQLALCHEMY_DATABASE_URI'))
