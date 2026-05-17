import os
import sys
from dotenv import load_dotenv
import mysql.connector

# Cargar variables de entorno
load_dotenv()

host = os.getenv("SBE_DB_HOST", "localhost")
port = os.getenv("SBE_DB_PORT", "3306")
user = os.getenv("SBE_DB_USER", "root")
password = os.getenv("SBE_DB_PASSWORD", "")

def seed_database():
    print(f"Conectando a MySQL en {host}:{port} con usuario '{user}'...")
    try:
        # Nos conectamos sin especificar la base de datos para poder crearla si no existe
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        # Lista de archivos a ejecutar en orden
        archivos_sql = [
            "db_brigadas_maracaibo.sql",
            "seed_super.sql",
            "migracion_v2_registro.sql",
            "migracion_actividad_creador.sql",
            "migracion_reportes.sql",
            "migrate_mensaje_dia.sql"
        ]
        
        for archivo in archivos_sql:
            sql_file = os.path.join("database", archivo)
            if not os.path.exists(sql_file):
                print(f"Advertencia: No se encontró el archivo {sql_file}, saltando...")
                continue
                
            print(f"Leyendo y ejecutando {sql_file}...")
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
                
            statements = []
            current_statement = ""
            for line in sql_script.splitlines():
                line = line.strip()
                if not line or line.startswith('--') or line.startswith('/*'):
                    continue
                current_statement += " " + line
                if line.endswith(';'):
                    statements.append(current_statement)
                    current_statement = ""
            
            for statement in statements:
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except mysql.connector.Error as err:
                        print(f"Ignorando error en sentencia de {archivo}: {err}")
                    
            conn.commit()
            
        print("¡Base de datos estructurada y migrada exitosamente!")
        
    except mysql.connector.Error as err:
        print(f"Error de base de datos: {err}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    seed_database()
