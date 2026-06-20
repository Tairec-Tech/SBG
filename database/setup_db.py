"""
setup_db.py — Montaje automático de la base de datos local para SBE.

Ejecuta en orden:
  1. db_brigadas_maracaibo.sql  (esquema + tablas)
  2. migracion_v2_registro.sql  (índices únicos)
  3. seed_super.sql             (datos de demostración)

Uso:
  python setup_db.py                  # Usa credenciales del .env
  python setup_db.py --force          # Borra y recrea la BD sin preguntar
  python setup_db.py --host localhost --port 3306 --user root --password ""
"""
import os
import sys
import argparse

# Resolver rutas relativas al script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# Cargar .env del proyecto
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(PROJECT_DIR, ".env"))
except ImportError:
    pass  # Si no tiene python-dotenv, usará args de línea de comando

# Archivos SQL en orden de ejecución
SQL_FILES = [
    os.path.join(SCRIPT_DIR, "db_brigadas_maracaibo.sql"),
    os.path.join(SCRIPT_DIR, "migracion_v2_registro.sql"),
    os.path.join(SCRIPT_DIR, "migracion_v3_media.sql"),
    os.path.join(SCRIPT_DIR, "seed_super.sql"),
]

SEPARATOR = "=" * 60


def print_step(step: int, total: int, msg: str):
    print(f"\n{SEPARATOR}")
    print(f"  [{step}/{total}] {msg}")
    print(SEPARATOR)


def connect_without_db(host: str, port: int, user: str, password: str):
    """Conecta a MySQL SIN seleccionar base de datos."""
    import mysql.connector
    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        charset="utf8mb4",
        use_pure=True,
        connection_timeout=10,
    )


def execute_sql_file(conn, filepath: str):
    """Lee y ejecuta un archivo .sql completo, sentencia por sentencia."""
    filename = os.path.basename(filepath)

    if not os.path.isfile(filepath):
        print(f"  ⚠  Archivo no encontrado: {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Separar sentencias por ';' (respetando que no estén dentro de strings)
    # Usamos un split simple que funciona para estos SQL en particular
    statements = []
    current = []
    for line in sql_content.splitlines():
        stripped = line.strip()
        # Ignorar comentarios puros y líneas vacías
        if stripped.startswith("--") or stripped.startswith("/*") or stripped == "":
            continue
        current.append(line)
        if stripped.endswith(";"):
            statements.append("\n".join(current))
            current = []
    # Sentencia final sin ';'
    if current:
        remaining = "\n".join(current).strip()
        if remaining:
            statements.append(remaining)

    cursor = conn.cursor()
    ejecutadas = 0
    errores = 0

    for stmt in statements:
        stmt_clean = stmt.strip()
        if not stmt_clean:
            continue
        try:
            cursor.execute(stmt_clean)
            ejecutadas += 1
        except Exception as e:
            error_msg = str(e)
            # Errores esperados que se pueden ignorar de forma segura
            ignorables = [
                "Duplicate key name",       # Índice ya existe
                "Duplicate entry",          # Dato ya insertado
                "already exists",           # Tabla/BD ya existe
                "1061",                     # Duplicate key name (código)
            ]
            if any(ign in error_msg for ign in ignorables):
                # Silenciar estos errores esperados
                pass
            else:
                preview = stmt_clean[:80].replace("\n", " ")
                print(f"  ⚠  Error en: {preview}...")
                print(f"       {e}")
                errores += 1

    conn.commit()
    cursor.close()
    print(f"  ✓  {filename}: {ejecutadas} sentencias ejecutadas", end="")
    if errores:
        print(f" ({errores} errores)")
    else:
        print()
    return errores == 0


def main():
    parser = argparse.ArgumentParser(
        description="Montaje automático de la BD local para SBE"
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("SBE_DB_HOST_LOCAL", "localhost"),
        help="Host de MySQL (default: del .env o localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("SBE_DB_PORT_LOCAL", "3306")),
        help="Puerto de MySQL (default: del .env o 3306)",
    )
    parser.add_argument(
        "--user",
        default=os.environ.get("SBE_DB_USER_LOCAL", "root"),
        help="Usuario de MySQL (default: del .env o root)",
    )
    parser.add_argument(
        "--password",
        default=os.environ.get("SBE_DB_PASSWORD_LOCAL", ""),
        help="Contraseña de MySQL (default: del .env o vacía)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ejecutar sin pedir confirmación",
    )
    args = parser.parse_args()

    print()
    print(SEPARATOR)
    print("  SBE — Setup automático de Base de Datos")
    print(SEPARATOR)
    print(f"  Host:     {args.host}:{args.port}")
    print(f"  Usuario:  {args.user}")
    print(f"  Password: {'***' if args.password else '(vacía)'}")
    print()

    # Verificar que los SQL existen
    for sql_path in SQL_FILES:
        if not os.path.isfile(sql_path):
            print(f"  ✗  No se encontró: {sql_path}")
            sys.exit(1)
        else:
            print(f"  ✓  {os.path.basename(sql_path)}")

    print()

    if not args.force:
        print("  ⚠  Esto BORRARÁ todos los datos existentes en db_brigadas_maracaibo")
        print("     y los reemplazará con los datos de demostración (seed).")
        print()
        respuesta = input("  ¿Continuar? (s/N): ").strip().lower()
        if respuesta not in ("s", "si", "sí", "y", "yes"):
            print("  Cancelado.")
            sys.exit(0)

    # Conectar a MySQL
    print_step(1, 3, "Conectando a MySQL...")
    try:
        conn = connect_without_db(args.host, args.port, args.user, args.password)
        print(f"  ✓  Conexión establecida ({args.host}:{args.port})")
    except Exception as e:
        print(f"  ✗  No se pudo conectar a MySQL: {e}")
        print()
        print("  Verifica que MySQL/XAMPP esté corriendo y que las credenciales")
        print("  en el .env sean correctas.")
        sys.exit(1)

    # Ejecutar los 3 SQL en orden
    total_steps = len(SQL_FILES)
    exito = True

    for i, sql_path in enumerate(SQL_FILES, start=1):
        nombre = os.path.basename(sql_path)
        print_step(i, total_steps + 1, f"Ejecutando {nombre}...")
        if not execute_sql_file(conn, sql_path):
            exito = False

    conn.close()

    # Resumen
    print()
    print(SEPARATOR)
    if exito:
        print("  ✓  BASE DE DATOS MONTADA EXITOSAMENTE")
        print()
        print("  Credenciales de prueba:")
        print("  ┌──────────────┬──────────────┬──────────────┐")
        print("  │ Usuario      │ Contraseña   │ Rol          │")
        print("  ├──────────────┼──────────────┼──────────────┤")
        print("  │ director     │ director123  │ Directivo    │")
        print("  │ profesor1    │ profesor1    │ Profesor     │")
        print("  │ profesor2    │ profesor2    │ Profesor     │")
        print("  │ ...          │ ...          │ ...          │")
        print("  │ profesor11   │ profesor11   │ Profesor     │")
        print("  └──────────────┴──────────────┴──────────────┘")
        print()
        print("  Institución: U.E. Libertador Simón Bolívar")
        print("  11 brigadas con 4 brigadistas cada una")
    else:
        print("  ⚠  Base de datos montada CON ADVERTENCIAS")
        print("     Revisa los errores arriba. El sistema podría funcionar")
        print("     parcialmente.")
    print(SEPARATOR)
    print()


if __name__ == "__main__":
    main()
