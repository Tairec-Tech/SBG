"""
CRUD de Brigada para el SBE.
Requiere haber ejecutado database/migrate_brigada_campos.sql si usas descripcion, coordinador, color.
"""
from database.connection import get_connection


def insertar_brigada(nombre, descripcion, coordinador, color_identificador, institucion_id, profesor_id=None, subjefe_id=None, tipo_brigada=None):
    """
    Inserta una nueva brigada.
    institucion_id: OBLIGATORIO (debe existir en Institucion_Educativa).
    profesor_id: ID del profesor responsable (NULL si no se asigna).
    subjefe_id: ID del brigadista (alumno) designado como sublíder (opcional).
    tipo_brigada: slug del tipo de brigada del catálogo oficial.
    Retorna el idBrigada creado o lanza excepción.
    """
    if not tipo_brigada:
        raise ValueError("tipo_brigada es obligatorio para crear una brigada.")
    conn = get_connection()
    try:
        cursor = conn.cursor()
        area_accion = (descripcion or nombre or "General")[:45]
        try:
            cursor.execute(
                """
                INSERT INTO brigada (
                    nombre_brigada, area_accion, descripcion, coordinador, color_identificador,
                    tipo_brigada, Institucion_Educativa_idInstitucion, profesor_id, subjefe_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (nombre, area_accion, descripcion or None, coordinador or None, color_identificador or None, tipo_brigada, institucion_id, profesor_id, subjefe_id),
            )
        except Exception as e:
            if "subjefe_id" in str(e) or "Unknown column" in str(e):
                cursor.execute(
                    """
                    INSERT INTO brigada (
                        nombre_brigada, area_accion, descripcion, coordinador, color_identificador,
                        tipo_brigada, Institucion_Educativa_idInstitucion, profesor_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (nombre, area_accion, descripcion or None, coordinador or None, color_identificador or None, tipo_brigada, institucion_id, profesor_id),
                )
            else:
                raise
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def listar_brigadas(tipo_brigada=None, brigada_rol_id=None, institucion_id=None, allow_global=False):
    """
    Lista brigadas con conteo de miembros, filtradas por institucion_id, brigada_rol_id o tipo_brigada.
    """
    if not (brigada_rol_id or institucion_id or tipo_brigada) and not allow_global:
        return []

    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        filtros = []
        params = []
        if brigada_rol_id is not None:
            filtros.append("b.idBrigada = %s")
            params.append(brigada_rol_id)
        elif institucion_id is not None:
            filtros.append("b.Institucion_Educativa_idInstitucion = %s")
            params.append(institucion_id)
            if tipo_brigada:
                filtros.append("b.tipo_brigada = %s")
                params.append(tipo_brigada)
        elif tipo_brigada:
            filtros.append("b.tipo_brigada = %s")
            params.append(tipo_brigada)
            
        filtro_str = ""
        if filtros:
            filtro_str = "WHERE " + " AND ".join(filtros)
            
        try:
            cursor.execute(
                f"""
                SELECT b.idBrigada, b.nombre_brigada, b.area_accion,
                    b.descripcion, b.coordinador, b.color_identificador, b.profesor_id,
                    p.nombre AS profesor_nombre, p.apellido AS profesor_apellido,
                    COUNT(u.idUsuario) AS num_miembros
                FROM brigada b
                LEFT JOIN usuario u ON u.Brigada_idBrigada = b.idBrigada
                LEFT JOIN usuario p ON p.idUsuario = b.profesor_id
                {filtro_str}
                GROUP BY b.idBrigada, b.nombre_brigada, b.area_accion, b.descripcion, b.coordinador, b.color_identificador,
                         b.profesor_id, p.nombre, p.apellido
                ORDER BY b.nombre_brigada
                """,
                params,
            )
        except Exception:
            try:
                cursor.execute(
                    f"""
                    SELECT b.idBrigada, b.nombre_brigada, b.area_accion,
                        b.descripcion, b.coordinador, b.color_identificador,
                        COUNT(u.idUsuario) AS num_miembros
                    FROM brigada b
                    LEFT JOIN usuario u ON u.Brigada_idBrigada = b.idBrigada
                    {filtro_str}
                    GROUP BY b.idBrigada, b.nombre_brigada, b.area_accion, b.descripcion, b.coordinador, b.color_identificador
                    ORDER BY b.nombre_brigada
                    """,
                    params,
                )
            except Exception:
                cursor.execute(
                    f"""
                    SELECT b.idBrigada, b.nombre_brigada, b.area_accion,
                        COUNT(u.idUsuario) AS num_miembros
                    FROM brigada b
                    LEFT JOIN usuario u ON u.Brigada_idBrigada = b.idBrigada
                    {filtro_str}
                    GROUP BY b.idBrigada, b.nombre_brigada, b.area_accion
                    ORDER BY b.nombre_brigada
                    """,
                    params,
                )
        rows = cursor.fetchall()
        for r in rows:
            r.setdefault("descripcion", None)
            r.setdefault("coordinador", None)
            r.setdefault("color_identificador", None)
            r.setdefault("profesor_id", None)
            r.setdefault("profesor_nombre", None)
            r.setdefault("profesor_apellido", None)
            r["num_miembros"] = r.get("num_miembros", 0) or 0
        return rows
    finally:
        conn.close()


def obtener_tipo_brigada_por_id(id_brigada: int):
    """Busca de forma ligera el tipo_brigada dado un ID. Retorna None si no tiene brigada."""
    if not id_brigada:
        return None
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT tipo_brigada FROM brigada WHERE idBrigada = %s", (id_brigada,))
            row = cursor.fetchone()
            if row and row.get("tipo_brigada"):
                return row["tipo_brigada"]
        except Exception:
            pass
        return None
    finally:
        conn.close()


def obtener_brigada(id_brigada: int):
    """Obtiene una brigada por id (con profesor_id y subjefe_id si existen). Retorna dict o None."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT idBrigada, nombre_brigada, area_accion, descripcion, coordinador, color_identificador,
                    Institucion_Educativa_idInstitucion, profesor_id, subjefe_id
                FROM brigada WHERE idBrigada = %s
                """,
                (id_brigada,),
            )
        except Exception:
            try:
                cursor.execute(
                    """
                    SELECT idBrigada, nombre_brigada, area_accion, descripcion, coordinador, color_identificador,
                        Institucion_Educativa_idInstitucion
                    FROM brigada WHERE idBrigada = %s
                    """,
                    (id_brigada,),
                )
            except Exception:
                cursor.execute(
                    "SELECT idBrigada, nombre_brigada, area_accion, Institucion_Educativa_idInstitucion FROM brigada WHERE idBrigada = %s",
                    (id_brigada,),
                )
        row = cursor.fetchone()
        if row:
            row.setdefault("descripcion", None)
            row.setdefault("coordinador", None)
            row.setdefault("color_identificador", None)
            row.setdefault("profesor_id", None)
            row.setdefault("subjefe_id", None)
        return row
    finally:
        conn.close()


def actualizar_brigada(id_brigada: int, nombre: str, area_accion: str = None, descripcion: str = None, coordinador: str = None, color_identificador: str = None, institucion_id: int = None):
    """Actualiza una brigada. area_accion es obligatorio en BD; si no se pasa, se usa nombre o 'General'."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        area = (area_accion or nombre or "General")[:45]
        try:
            cursor.execute(
                """
                UPDATE brigada SET nombre_brigada = %s, area_accion = %s, descripcion = %s, coordinador = %s, color_identificador = %s
                WHERE idBrigada = %s
                """,
                (nombre, area, descripcion or None, coordinador or None, color_identificador or None, id_brigada),
            )
        except Exception:
            cursor.execute(
                "UPDATE brigada SET nombre_brigada = %s, area_accion = %s WHERE idBrigada = %s",
                (nombre, area, id_brigada),
            )
        conn.commit()
    finally:
        conn.close()


def eliminar_brigada(id_brigada: int) -> str | None:
    """
    Elimina la brigada si no tiene usuarios asignados.
    Retorna None si OK, o mensaje de error si tiene miembros o fallo.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE Brigada_idBrigada = %s", (id_brigada,))
        (num,) = cursor.fetchone()
        if num and num > 0:
            return f"No se puede eliminar: la brigada tiene {num} usuario(s) asignado(s). Asigne o elimine los usuarios primero."
        cursor.execute("DELETE FROM brigada WHERE idBrigada = %s", (id_brigada,))
        conn.commit()
        return None
    except Exception as e:
        error_msg = str(e)
        if "foreign key constraint fails" in error_msg.lower() or "cannot delete or update a parent row" in error_msg.lower():
            return "No se puede eliminar: La brigada tiene Actividades o Turnos registrados."
        return error_msg
    finally:
        conn.close()


def listar_brigadas_para_profesor(profesor_id: int, institucion_id: int, tipo_brigada=None):
    """
    Lista brigadas visibles para un profesor, filtradas por tipo_brigada.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        filtro_tipo = ""
        params = [institucion_id, profesor_id]
        if tipo_brigada:
            filtro_tipo = "AND b.tipo_brigada = %s"
            params.append(tipo_brigada)
        cursor.execute(
            f"""
            SELECT b.idBrigada, b.nombre_brigada, b.area_accion,
                   b.descripcion, b.coordinador, b.color_identificador, b.profesor_id,
                   COUNT(u.idUsuario) AS num_miembros,
                   p.nombre AS profesor_nombre, p.apellido AS profesor_apellido
            FROM brigada b
            LEFT JOIN usuario u ON u.Brigada_idBrigada = b.idBrigada
            LEFT JOIN usuario p ON p.idUsuario = b.profesor_id
            WHERE b.Institucion_Educativa_idInstitucion = %s
              AND b.profesor_id = %s
              {filtro_tipo}
            GROUP BY b.idBrigada, b.nombre_brigada, b.area_accion, b.descripcion, 
                     b.coordinador, b.color_identificador, b.profesor_id,
                     p.nombre, p.apellido
            ORDER BY b.nombre_brigada
            """,
            tuple(params),
        )
        rows = cursor.fetchall()
        for r in rows:
            r.setdefault("descripcion", None)
            r.setdefault("coordinador", None)
            r.setdefault("color_identificador", None)
            r["num_miembros"] = r.get("num_miembros", 0) or 0
            r["es_propia"] = r.get("profesor_id") == profesor_id
        return rows
    finally:
        conn.close()


def listar_brigadas_por_institucion(institucion_id: int, solo_sin_profesor: bool = False):
    """
    Lista brigadas de una institución.
    Si solo_sin_profesor=True, retorna solo brigadas sin profesor responsable.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        filtro_prof = "AND b.profesor_id IS NULL" if solo_sin_profesor else ""
        cursor.execute(
            f"""
            SELECT b.idBrigada, b.nombre_brigada, b.tipo_brigada, b.color_identificador,
                   b.profesor_id, b.area_accion, b.descripcion,
                   p.nombre AS profesor_nombre, p.apellido AS profesor_apellido
            FROM brigada b
            LEFT JOIN usuario p ON p.idUsuario = b.profesor_id
            WHERE b.Institucion_Educativa_idInstitucion = %s
            {filtro_prof}
            ORDER BY b.nombre_brigada
            """,
            (institucion_id,),
        )
        return cursor.fetchall()
    finally:
        conn.close()


def asignar_profesor_a_brigada(brigada_id: int, profesor_id: int):
    """
    Asigna un profesor como responsable de una brigada.
    Actualiza AMBOS lados: brigada.profesor_id y usuario.Brigada_idBrigada.
    Valida: misma institución, brigada sin profesor actual, profesor sin brigada actual.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        # Leer brigada
        cursor.execute(
            "SELECT idBrigada, profesor_id, Institucion_Educativa_idInstitucion FROM brigada WHERE idBrigada = %s",
            (brigada_id,),
        )
        brigada = cursor.fetchone()
        if not brigada:
            raise ValueError("La brigada no existe.")
        if brigada.get("profesor_id"):
            raise ValueError("Esta brigada ya tiene un profesor responsable. Desasigne primero.")
        # Leer profesor
        cursor.execute(
            "SELECT idUsuario, Brigada_idBrigada, Institucion_Educativa_idInstitucion FROM usuario WHERE idUsuario = %s AND rol = 'Profesor'",
            (profesor_id,),
        )
        profesor = cursor.fetchone()
        if not profesor:
            raise ValueError("El profesor no existe o no tiene rol Profesor.")
        # Validar misma institución
        if brigada.get("Institucion_Educativa_idInstitucion") != profesor.get("Institucion_Educativa_idInstitucion"):
            raise ValueError("El profesor no pertenece a la misma institución que la brigada.")
        # Validar que profesor no tenga otra brigada
        if profesor.get("Brigada_idBrigada"):
            raise ValueError("Este profesor ya está asignado a otra brigada.")
        # Transacción: actualizar ambos lados
        conn.start_transaction()
        cursor.execute("UPDATE brigada SET profesor_id = %s WHERE idBrigada = %s", (profesor_id, brigada_id))
        cursor.execute("UPDATE usuario SET Brigada_idBrigada = %s WHERE idUsuario = %s", (brigada_id, profesor_id))
        conn.commit()
    except Exception:
        try:
            conn.rollback()
        except Exception:
            pass
        raise
    finally:
        conn.close()


def desasignar_profesor_de_brigada(brigada_id: int):
    """
    Desasigna el profesor responsable de una brigada.
    Limpia AMBOS lados: brigada.profesor_id y usuario.Brigada_idBrigada.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT profesor_id FROM brigada WHERE idBrigada = %s", (brigada_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError("La brigada no existe.")
        profesor_anterior = row.get("profesor_id")
        if not profesor_anterior:
            return  # Ya no tiene profesor, nada que hacer
        conn.start_transaction()
        cursor.execute("UPDATE usuario SET Brigada_idBrigada = NULL WHERE idUsuario = %s", (profesor_anterior,))
        cursor.execute("UPDATE brigada SET profesor_id = NULL WHERE idBrigada = %s", (brigada_id,))
        conn.commit()
    except Exception:
        try:
            conn.rollback()
        except Exception:
            pass
        raise
    finally:
        conn.close()


def reemplazar_profesor_brigada(brigada_id: int, nuevo_profesor_id: int):
    """
    Reemplaza el profesor responsable de una brigada en una sola transacción.
    Desasigna el anterior (si existe) y asigna el nuevo.
    Valida: misma institución, nuevo profesor sin brigada actual, no duplicado.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        # Leer brigada
        cursor.execute(
            "SELECT idBrigada, profesor_id, Institucion_Educativa_idInstitucion FROM brigada WHERE idBrigada = %s",
            (brigada_id,),
        )
        brigada = cursor.fetchone()
        if not brigada:
            raise ValueError("La brigada no existe.")
        # Leer nuevo profesor
        cursor.execute(
            "SELECT idUsuario, Brigada_idBrigada, Institucion_Educativa_idInstitucion FROM usuario WHERE idUsuario = %s AND rol = 'Profesor'",
            (nuevo_profesor_id,),
        )
        nuevo_prof = cursor.fetchone()
        if not nuevo_prof:
            raise ValueError("El profesor no existe o no tiene rol Profesor.")
        # Validar misma institución
        if brigada.get("Institucion_Educativa_idInstitucion") != nuevo_prof.get("Institucion_Educativa_idInstitucion"):
            raise ValueError("El profesor no pertenece a la misma institución que la brigada.")
        # Validar que nuevo profesor no tenga ya brigada
        if nuevo_prof.get("Brigada_idBrigada"):
            raise ValueError("Este profesor ya está asignado a otra brigada. Desasígnelo primero.")
        # Validar que no esté ya como profesor_id en otra brigada
        cursor.execute(
            "SELECT idBrigada FROM brigada WHERE profesor_id = %s AND idBrigada != %s",
            (nuevo_profesor_id, brigada_id),
        )
        otra = cursor.fetchone()
        if otra:
            raise ValueError(f"Este profesor ya es responsable de otra brigada (ID {otra['idBrigada']}).")
        profesor_anterior = brigada.get("profesor_id")
        # Transacción
        conn.start_transaction()
        # Desasignar anterior si existe
        if profesor_anterior:
            cursor.execute("UPDATE usuario SET Brigada_idBrigada = NULL WHERE idUsuario = %s", (profesor_anterior,))
        # Asignar nuevo
        cursor.execute("UPDATE brigada SET profesor_id = %s WHERE idBrigada = %s", (nuevo_profesor_id, brigada_id))
        cursor.execute("UPDATE usuario SET Brigada_idBrigada = %s WHERE idUsuario = %s", (brigada_id, nuevo_profesor_id))
        conn.commit()
    except Exception:
        try:
            conn.rollback()
        except Exception:
            pass
        raise
    finally:
        conn.close()
