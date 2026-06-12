"""
Conexión a MySQL para el SBE — con connection pool.

Cambios clave vs. versión anterior:
- Las credenciales se leen LAZY desde get_db_config() al crear el pool.
- SSL es condicional: solo se activa en modo producción.
- Todos los errores se registran en sbe_log.txt vía util_log.log().
"""
import os
import sys
from time import perf_counter

import mysql.connector
from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool

from database.config import get_db_config
from util_log import log


if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SSL_CA_PATH = os.path.join(BASE_DIR, "ca.pem")

# Pool global: reutiliza conexiones en vez de abrir/cerrar cada vez
_pool = None


def _get_pool():
    """Inicializa el pool de conexiones (lazy, una sola vez)."""
    global _pool
    if _pool is None:
        cfg = get_db_config()
        log(f"[DB] Creando pool — host={cfg['host']}:{cfg['port']} "
            f"db={cfg['database']} user={cfg['user']} ssl={cfg['use_ssl']}")

        pool_kwargs = dict(
            pool_name="sbe_pool",
            pool_size=5,
            pool_reset_session=True,
            host=cfg["host"],
            port=cfg["port"],
            user=cfg["user"],
            password=cfg["password"],
            database=cfg["database"],
            charset="utf8mb4",
            connection_timeout=10,
            use_pure=True,  # Previene errores de extensión C en empaquetado
        )

        # SSL solo para producción (Aiven); local (XAMPP) no lo soporta
        if cfg["use_ssl"] and os.path.isfile(SSL_CA_PATH):
            pool_kwargs["ssl_ca"] = SSL_CA_PATH
            pool_kwargs["ssl_disabled"] = False
            log(f"[DB] SSL activado con ca.pem: {SSL_CA_PATH}")
        else:
            pool_kwargs["ssl_disabled"] = True
            if cfg["use_ssl"]:
                log(f"[DB] ADVERTENCIA: SSL solicitado pero ca.pem no encontrado en {SSL_CA_PATH}")
            else:
                log("[DB] SSL desactivado (modo local)")

        try:
            _pool = MySQLConnectionPool(**pool_kwargs)
            log("[DB] Pool creado exitosamente")
        except Error as e:
            log(f"[DB] ERROR al crear pool: {e}")
            raise RuntimeError(f"Error al crear pool de conexiones: {e}") from e
    return _pool


def get_connection():
    """Obtiene una conexión del pool. Cerrar con conn.close() (la devuelve al pool)."""
    try:
        return _get_pool().get_connection()
    except Error as e:
        log(f"[DB] ERROR al obtener conexión del pool: {e}")
        raise RuntimeError(f"Error al conectar a la base de datos: {e}") from e


def ejecutar(consulta, params=None, commit=False):
    """
    Ejecuta una consulta.
    Si commit=True: hace commit y retorna lastrowid. Cierra conexión.
    Si commit=False: hace fetchall y retorna (rows, description). Cierra conexión.
    """
    t0 = perf_counter()
    conn = get_connection()
    t_conn = perf_counter()
    try:
        cursor = conn.cursor()
        cursor.execute(consulta, params or ())
        t_exec = perf_counter()
        if commit:
            conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            t_fetch = perf_counter()
            log(f"[DB] conn={t_conn-t0:.3f}s exec={t_exec-t_conn:.3f}s fetch={t_fetch-t_exec:.3f}s total={t_fetch-t0:.3f}s | Q: {consulta.strip()[:60]}...")
            return last_id
        else:
            rows = cursor.fetchall()
            description = cursor.description
            cursor.close()
            t_fetch = perf_counter()
            log(f"[DB] conn={t_conn-t0:.3f}s exec={t_exec-t_conn:.3f}s fetch={t_fetch-t_exec:.3f}s total={t_fetch-t0:.3f}s | Q: {consulta.strip()[:60]}...")
            return rows, description
    except Error as e:
        log(f"[DB] ERROR en consulta: {e} | Q: {consulta.strip()[:80]}")
        raise
    finally:
        if conn.is_connected():
            conn.close()


def ejecutar_modificar(consulta, params=None):
    """
    Ejecuta un UPDATE o DELETE y retorna el número de filas afectadas (rowcount).
    Hace commit automáticamente.
    """
    t0 = perf_counter()
    conn = get_connection()
    t_conn = perf_counter()
    try:
        cursor = conn.cursor()
        cursor.execute(consulta, params or ())
        t_exec = perf_counter()
        conn.commit()
        afectadas = cursor.rowcount
        cursor.close()
        t_fetch = perf_counter()
        log(f"[DB] conn={t_conn-t0:.3f}s exec={t_exec-t_conn:.3f}s commit={t_fetch-t_exec:.3f}s total={t_fetch-t0:.3f}s | Q: {consulta.strip()[:60]}...")
        return afectadas
    except Error as e:
        log(f"[DB] ERROR en modificación: {e} | Q: {consulta.strip()[:80]}")
        raise
    finally:
        if conn.is_connected():
            conn.close()
