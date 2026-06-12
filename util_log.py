"""
Log a archivo para ver qué pasa cuando la terminal no muestra nada.
En modo .exe el archivo sbe_log.txt se crea junto al ejecutable.
En modo desarrollo se crea en la carpeta del proyecto.
"""
import os
import sys
from datetime import datetime

if getattr(sys, 'frozen', False):
    # .exe empaquetado: escribir junto al ejecutable
    _log_dir = os.path.dirname(sys.executable)
else:
    _log_dir = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(_log_dir, "sbe_log.txt")


def log(mensaje: str):
    """Escribe una línea con fecha/hora en sbe_log.txt (y hace flush)."""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensaje}\n")
            f.flush()
    except Exception:
        pass
