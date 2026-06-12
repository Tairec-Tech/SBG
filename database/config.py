"""
Configuración de la base de datos MySQL.
Usa variables de entorno o el archivo .env en la raíz del proyecto.
El sistema soporta SBE_ENV=local|production para aislamiento de BBDD.

IMPORTANTE: Las credenciales se leen de forma LAZY (al invocar get_db_config())
para garantizar que main.py ya haya cargado el .env antes de la primera lectura.
"""
import os
import sys

from dotenv import load_dotenv


def _ensure_dotenv():
    """Carga .env si aún no se ha cargado. Idempotente."""
    if getattr(sys, 'frozen', False):
        env_path = os.path.join(os.path.dirname(sys.executable), '.env')
    else:
        env_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            '.env',
        )
    load_dotenv(env_path)


def get_db_config() -> dict:
    """
    Retorna un dict con las credenciales de conexión a la BD.
    Se evalúa en el momento de la llamada, NO al importar el módulo.

    Claves retornadas:
        host, port, user, password, database, use_ssl
    """
    _ensure_dotenv()

    sbe_env = os.environ.get("SBE_ENV", "local").lower()

    if sbe_env == "production":
        return {
            "host":     os.environ.get("SBE_DB_HOST_PROD", "localhost"),
            "port":     int(os.environ.get("SBE_DB_PORT_PROD", "3306")),
            "user":     os.environ.get("SBE_DB_USER_PROD", "root"),
            "password": os.environ.get("SBE_DB_PASSWORD_PROD", ""),
            "database": os.environ.get("SBE_DB_NAME_PROD", "db_brigadas_maracaibo"),
            "use_ssl":  True,
        }
    else:
        return {
            "host":     os.environ.get("SBE_DB_HOST_LOCAL", "localhost"),
            "port":     int(os.environ.get("SBE_DB_PORT_LOCAL", "3306")),
            "user":     os.environ.get("SBE_DB_USER_LOCAL", "root"),
            "password": os.environ.get("SBE_DB_PASSWORD_LOCAL", ""),
            "database": os.environ.get("SBE_DB_NAME_LOCAL", "db_brigadas_maracaibo"),
            "use_ssl":  False,
        }


# ── Compatibilidad retroactiva ──────────────────────────────────────────
# Algunos módulos importan DB_HOST, DB_PORT, etc. directamente.
# Estos valores se resuelven al importar, pero config.py ahora
# se importa DESPUÉS de que main.py haga load_dotenv().
_ensure_dotenv()
_sbe_env = os.environ.get("SBE_ENV", "local").lower()

if _sbe_env == "production":
    DB_HOST     = os.environ.get("SBE_DB_HOST_PROD", "localhost")
    DB_PORT     = int(os.environ.get("SBE_DB_PORT_PROD", "3306"))
    DB_USER     = os.environ.get("SBE_DB_USER_PROD", "root")
    DB_PASSWORD = os.environ.get("SBE_DB_PASSWORD_PROD", "")
    DB_NAME     = os.environ.get("SBE_DB_NAME_PROD", "db_brigadas_maracaibo")
else:
    DB_HOST     = os.environ.get("SBE_DB_HOST_LOCAL", "localhost")
    DB_PORT     = int(os.environ.get("SBE_DB_PORT_LOCAL", "3306"))
    DB_USER     = os.environ.get("SBE_DB_USER_LOCAL", "root")
    DB_PASSWORD = os.environ.get("SBE_DB_PASSWORD_LOCAL", "")
    DB_NAME     = os.environ.get("SBE_DB_NAME_LOCAL", "db_brigadas_maracaibo")
