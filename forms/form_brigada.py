"""
Formularios CRUD del SBE — brigadas ambientales (tonos verdes).
"""

import flet as ft

from database.crud_brigada import insertar_brigada, actualizar_brigada, eliminar_brigada, obtener_brigada, listar_brigadas
from database.crud_usuario import (
    crear_usuario, email_ya_existe, cedula_ya_existe, obtener_id_usuario_por_cedula,
    listar_brigadistas, actualizar_usuario, eliminar_usuario, obtener_usuario,
    es_admin, es_profesor, listar_profesores_institucion, listar_alumnos_del_profesor,
    usuario_ya_existe,
)
from theme import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_BORDE,
    COLOR_CARD,
    COLOR_CANCELAR,
)
RADIO = 12
PADDING = 20
# Dimensiones del contenedor del formulario (modal)
ANCHO_FORM = 520
ALTURA_MAX_FORM = 480
# Nueva Brigada: contenedor más compacto, alineado a la imagen
ANCHO_FORM_NUEVA_BRIGADA = 400
PADDING_NUEVA_BRIGADA = 20
ALTURA_BOTON_NUEVA_BRIGADA = 52
# Estilo común para campos (alineado a Figma)
_CAMPO_PADDING = ft.Padding(14, 16)
_CAMPO_BASE = dict(
    border_color=COLOR_BORDE,
    focused_border_color=COLOR_PRIMARIO,
    border_radius=RADIO,
    text_size=14,
    color=COLOR_TEXTO,
    hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
    cursor_color=COLOR_PRIMARIO,
    content_padding=_CAMPO_PADDING,
)
# Dropdown no soporta cursor_color en Flet 0.80.5
_DROPDOWN_BASE = {k: v for k, v in _CAMPO_BASE.items() if k != "cursor_color"}


from forms.common import _etiqueta, _campo_texto, _campo_numero, _selector, _bloque_campo, _campo_con_titulo, _cerrar_dialogo, _on_cancelar, _dialogo_formulario, _abrir_dialogo, _obtener_brigadas_form

def abrir_form_brigada_registrar(page: ft.Page, on_success=None, usuario_actual=None):
    """
    DESHABILITADA: Las brigadas se crean automáticamente al registrar la institución.
    No se permite crear brigadas fuera del catálogo institucional de 11.
    """
    page.snack_bar = ft.SnackBar(
        ft.Text("Las brigadas se crean automáticamente al registrar la institución. No es posible crear brigadas adicionales."),
        bgcolor="#ef4444",
    )
    page.snack_bar.open = True
    page.update()


def abrir_form_brigada_modificar(page: ft.Page, brigada=None, on_success=None):
    """Abre el formulario de modificar brigada. Si brigada (dict) se pasa, precarga datos y al guardar actualiza en BD y llama on_success()."""
    from database.crud_usuario import listar_estudiantes_por_brigada
    id_brigada_val = brigada.get("idBrigada") if brigada else None
    nombre = ft.TextField(
        label="Nombre",
        hint_text="Nombre de la brigada",
        value=brigada.get("nombre_brigada", "") if brigada else "",
        **_CAMPO_BASE,
    )
    area_accion = ft.TextField(
        label="Área de acción",
        hint_text="Área de acción",
        value=brigada.get("area_accion", "") if brigada else "",
        **_CAMPO_BASE,
    )
    descripcion = ft.TextField(
        label="Descripción",
        hint_text="Descripción (opcional)",
        value=brigada.get("descripcion") or "" if brigada else "",
        multiline=True,
        min_lines=2,
        **_CAMPO_BASE,
    )
    try:
        estudiantes = listar_estudiantes_por_brigada(id_brigada_val) if id_brigada_val else []
    except Exception:
        estudiantes = []
        
    opciones_subjefe = [ft.dropdown.Option("", "Sin sub-líder")]
    for est in estudiantes:
        opciones_subjefe.append(ft.dropdown.Option(str(est["idUsuario"]), f"{est.get('nombre', '')} {est.get('apellido', '')} ({est.get('email', '')})"))
        
    subjefe_id_val = str(brigada.get("subjefe_id") or "") if brigada and brigada.get("subjefe_id") else ""
    coordinador = ft.Dropdown(
        label="Sub-líder",
        hint_text="Seleccione un estudiante registrado",
        options=opciones_subjefe,
        value=subjefe_id_val,
        **_DROPDOWN_BASE,
    )

    def on_guardar(_):
        if not id_brigada_val:
            page.snack_bar = ft.SnackBar(ft.Text("Error: no se identificó la brigada"))
            page.snack_bar.open = True
            page.update()
            return
        nom = (nombre.value or "").strip()
        if not nom:
            page.snack_bar = ft.SnackBar(ft.Text("El nombre es obligatorio"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        try:
            
            subjefe_id_parsed = None
            if coordinador.value and coordinador.value.strip():
                try:
                    subjefe_id_parsed = int(coordinador.value)
                except ValueError:
                    pass

            actualizar_brigada(
                id_brigada=id_brigada_val,
                nombre=nom,
                area_accion=(area_accion.value or "").strip() or None,
                descripcion=(descripcion.value or "").strip() or None,
                subjefe_id=subjefe_id_parsed,
            )
            _cerrar_dialogo(page)
            page.snack_bar = ft.SnackBar(ft.Text("¡Brigada actualizada correctamente!"), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success:
                on_success()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="#ef4444")
            page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text(f"ID Brigada: {id_brigada_val}", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=12),
            nombre,
            ft.Container(height=12),
            area_accion,
            ft.Container(height=12),
            descripcion,
            ft.Container(height=12),
            coordinador,
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Modificar brigada", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_brigada_consultar(page: ft.Page):
    id_brigada = _campo_numero("ID Brigada", "Consultar por ID")
    resultado = ft.Text("Ingrese ID y pulse Buscar.", size=13, color=COLOR_TEXTO_SEC)

    def on_buscar(_):
        resultado.value = f"Consulta brigada ID {id_brigada.value or '(vacío)'} (pendiente conectar BD)."
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Brigada", id_brigada),
            ft.Container(height=12),
            ft.ElevatedButton("Buscar", on_click=on_buscar, style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO)),
            ft.Container(height=12),
            resultado,
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Consultar brigada", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=420, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_TEXTO), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_form_brigada_eliminar(page: ft.Page, brigada=None, on_success=None):
    """Abre el diálogo de confirmación para eliminar. Si brigada (dict) se pasa, muestra nombre y al confirmar elimina en BD y llama on_success()."""
    id_brigada_val = brigada.get("idBrigada") if brigada else None
    nombre_brigada = (brigada.get("nombre_brigada") or "esta brigada") if brigada else ""

    def on_eliminar(_):
        if not id_brigada_val:
            page.snack_bar = ft.SnackBar(ft.Text("Error: no se identificó la brigada", color="white"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return

        # 1. Ejecutar acción en BD
        err = eliminar_brigada(id_brigada_val)

        # 2. Cerrar el modal y FORZAR la actualización visual
        _cerrar_dialogo(page)
        page.update()

        # 3. Micro-pausa no bloqueante para aislar los updates de Flet (condición de carrera)
        import threading
        import time

        def show_msg():
            time.sleep(0.2)
            if err:
                page.snack_bar = ft.SnackBar(ft.Text(err, color="white"), bgcolor="#ef4444")
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Brigada eliminada correctamente", color="white"), bgcolor="#22c55e")
                if on_success:
                    on_success()
            page.snack_bar.open = True
            page.update()

        threading.Thread(target=show_msg).start()

    contenido = ft.Column(
        [
            ft.Text("Eliminar una brigada puede afectar actividades y usuarios asociados. Solo se puede eliminar si no tiene usuarios asignados.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            ft.Text(f"¿Eliminar la brigada «{nombre_brigada}» (ID {id_brigada_val})?", size=14, weight="w600", color=COLOR_TEXTO),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Eliminar brigada", contenido, on_guardar=on_eliminar, texto_guardar="Eliminar")
    _abrir_dialogo(page, dialogo)


def abrir_form_brigada_agregar_miembros(page: ft.Page, brigada=None, on_success=None):
    """Abre el diálogo para agregar miembros a una brigada. Lista usuarios de otras brigadas y permite asignarlos a esta."""
    if not brigada:
        page.snack_bar = ft.SnackBar(ft.Text("Error: no se especificó la brigada"))
        page.snack_bar.open = True
        page.update()
        return
    id_brigada = brigada.get("idBrigada")
    nombre_brigada = brigada.get("nombre_brigada") or f"Brigada {id_brigada}"
    try:
        todos = listar_brigadistas()
    except Exception:
        todos = []
    miembros_actuales = [u for u in todos if (u.get("Brigada_idBrigada") or 0) == id_brigada]
    disponibles = [u for u in todos if (u.get("Brigada_idBrigada") or 0) != id_brigada]
    opciones_dropdown = [
        ft.dropdown.Option(
            str(u["idUsuario"]),
            f"{u.get('nombre', '')} {u.get('apellido', '')} — {u.get('nombre_brigada') or 'Sin brigada'}",
        )
        for u in disponibles
    ]
    selector_usuario = ft.Dropdown(
        hint_text="Seleccione un usuario para agregar a esta brigada",
        options=opciones_dropdown,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        text_size=14,
        color=COLOR_TEXTO,
        content_padding=_CAMPO_PADDING,
    )

    def on_agregar(_):
        val = selector_usuario.value
        if not val:
            page.snack_bar = ft.SnackBar(ft.Text("Seleccione un usuario"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        id_usuario = int(val)
        usuario = obtener_usuario(id_usuario)
        if not usuario:
            page.snack_bar = ft.SnackBar(ft.Text("Usuario no encontrado"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        try:
            actualizar_usuario(
                id_usuario,
                nombre=usuario.get("nombre") or "",
                apellido=usuario.get("apellido") or "",
                email=usuario.get("email") or "",
                rol=usuario.get("rol") or "Brigadista",
                brigada_id=id_brigada,
            )
            _cerrar_dialogo(page)
            page.snack_bar = ft.SnackBar(ft.Text("¡Miembro agregado a la brigada!"), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success:
                on_success()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="#ef4444")
            page.snack_bar.open = True
        page.update()

    lista_actuales = ft.Column(
        [
            ft.Text("Miembros actuales", size=14, weight="w600", color=COLOR_TEXTO),
            ft.Container(height=8),
            *(
                [
                    ft.Container(
                        content=ft.Text(f"• {u.get('nombre', '')} {u.get('apellido', '')} ({u.get('email', '')})", size=13, color=COLOR_TEXTO_SEC),
                        padding=ft.Padding(0, 4),
                    )
                    for u in miembros_actuales
                ]
                if miembros_actuales
                else [ft.Text("Ninguno aún.", size=13, color=COLOR_TEXTO_SEC)]
            ),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )
    bloques_agregar = [
        ft.Text("Usuario a agregar", size=14, weight="w500", color=COLOR_TEXTO),
        ft.Container(height=8),
        selector_usuario,
        ft.Container(height=16),
        ft.Row(
            [
                ft.FilledButton(
                    "Agregar a esta brigada",
                    style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, shape=ft.RoundedRectangleBorder(radius=RADIO)),
                    on_click=on_agregar,
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
        ),
    ]
    if not disponibles:
        bloques_agregar = [
            ft.Text("No hay usuarios de otras brigadas para agregar. Cree brigadistas en otras brigadas o regístrelos desde «Brigadistas».", size=13, color=COLOR_TEXTO_SEC),
        ]
    contenido = ft.Column(
        [
            ft.Text(f"Agregar miembros a «{nombre_brigada}». Los usuarios de otras brigadas pueden reasignarse aquí.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            lista_actuales,
            ft.Container(height=20),
            *bloques_agregar,
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Agregar miembros", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=440, bgcolor=COLOR_CARD),
        actions=[
            ft.TextButton(
                content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500),
                style=ft.ButtonStyle(color=COLOR_CANCELAR),
                on_click=lambda e: _cerrar_dialogo(e.page),
            ),
        ],
    )
    _abrir_dialogo(page, dialogo)


# ---------- Nuevo Brigadista (solo desde Brigadistas: registrar alumno) ----------
def abrir_form_brigada_asignar(page: ft.Page):
    id_brigada = _campo_numero("ID Brigada", "")
    id_actividad = _campo_numero("ID Actividad", "Actividad a asignar (opcional)")
    id_institucion = _campo_numero("ID Institución", "Institución (opcional)")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Asignación registrada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text("Asignar brigada a actividad o institución.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            _bloque_campo("ID Brigada", id_brigada),
            ft.Container(height=12),
            _bloque_campo("ID Actividad", id_actividad),
            ft.Container(height=12),
            _bloque_campo("ID Institución", id_institucion),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Asignar brigada", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_brigada_miembros(page: ft.Page):
    id_brigada = _campo_numero("ID Brigada", "Ver o gestionar miembros")

    def on_buscar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Listado de miembros (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Brigada", id_brigada),
            ft.Container(height=12),
            ft.ElevatedButton("Ver miembros", on_click=on_buscar, style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO)),
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Gestionar miembros de brigada", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=420, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_TEXTO), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


# ---------- Actividades (5.0) ----------
# Actividad: estado, titulo, descripcion, fecha_inicio, fecha_fin, Brigada_idBrigada


def abrir_form_asignar_profesor_brigada(page: ft.Page, brigada: dict, on_success=None):
    """
    Formulario para asignar o reemplazar profesor responsable de una brigada.
    Si la brigada ya tiene profesor, muestra opción de reemplazo con confirmación.
    """
    from database.crud_usuario import listar_profesores_institucion
    from database.crud_brigada import asignar_profesor_a_brigada, reemplazar_profesor_brigada

    usuario_actual = {}
    try:
        if getattr(page, "data", None) and isinstance(page.data.get("usuario_actual"), dict):
            usuario_actual = page.data["usuario_actual"]
    except Exception:
        pass
    institucion_id = usuario_actual.get("institucion_id")
    if not institucion_id:
        page.snack_bar = ft.SnackBar(ft.Text("No se encontró la institución del usuario actual."), bgcolor="#ef4444")
        page.snack_bar.open = True
        page.update()
        return

    brigada_id = brigada.get("idBrigada")
    profesor_actual = brigada.get("profesor_id")
    nombre_prof_actual = ""
    if profesor_actual:
        pnom = (brigada.get("profesor_nombre") or "").strip()
        pap = (brigada.get("profesor_apellido") or "").strip()
        nombre_prof_actual = f"{pnom} {pap}".strip() or f"ID {profesor_actual}"

    # Cargar profesores sin brigada
    try:
        profesores_disp = listar_profesores_institucion(institucion_id, solo_sin_brigada=True)
    except Exception:
        profesores_disp = []

    if not profesores_disp and not profesor_actual:
        page.snack_bar = ft.SnackBar(ft.Text("No hay profesores disponibles sin brigada asignada."), bgcolor="#ef4444")
        page.snack_bar.open = True
        page.update()
        return

    opciones = [ft.dropdown.Option(str(p["idUsuario"]), f"{p.get('nombre', '')} {p.get('apellido', '')}") for p in profesores_disp]
    dropdown_profesor = ft.Dropdown(
        hint_text="Seleccione un profesor",
        options=opciones,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        text_size=14,
        color=COLOR_TEXTO,
        content_padding=ft.Padding(12, 14),
        border_radius=RADIO,
        dense=True,
    )

    info_actual = []
    if profesor_actual:
        info_actual = [
            ft.Container(
                content=ft.Column([
                    ft.Text("Profesor actual:", size=13, weight="w500", color=COLOR_TEXTO_SEC),
                    ft.Text(nombre_prof_actual, size=14, weight="w600", color=COLOR_TEXTO),
                    ft.Text("Se reemplazará al asignar un nuevo profesor.", size=12, color="#ef4444", italic=True),
                ], spacing=4),
                padding=ft.Padding(12, 12, 12, 12),
                border_radius=8,
                bgcolor=ft.Colors.with_opacity(0.1, "#ef4444"),
            ),
            ft.Container(height=12),
        ]

    def on_asignar(_):
        if not dropdown_profesor.value:
            page.snack_bar = ft.SnackBar(ft.Text("Seleccione un profesor."), bgcolor="#ef4444")
            page.snack_bar.open = True; page.update(); return
        nuevo_id = int(dropdown_profesor.value)
        try:
            if profesor_actual:
                reemplazar_profesor_brigada(brigada_id, nuevo_id)
            else:
                asignar_profesor_a_brigada(brigada_id, nuevo_id)
            _cerrar_dialogo(page)
            page.snack_bar = ft.SnackBar(ft.Text("¡Profesor asignado correctamente!"), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success:
                on_success()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="#ef4444")
            page.snack_bar.open = True
        page.update()

    titulo = "Reemplazar Profesor Responsable" if profesor_actual else "Asignar Profesor Responsable"
    btn_texto = "Reemplazar" if profesor_actual else "Asignar"

    contenido = ft.Container(
        content=ft.Column(
            [
                *info_actual,
                _campo_con_titulo("Nuevo profesor *", dropdown_profesor),
            ],
            spacing=0,
        ),
        padding=PADDING,
        width=ANCHO_FORM,
    )

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text(titulo, size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=ANCHO_FORM, height=300, bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: _cerrar_dialogo(page), style=ft.ButtonStyle(color=COLOR_TEXTO)),
            ft.FilledButton(btn_texto, on_click=on_asignar, style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, color="white")),
        ],
    )
    _abrir_dialogo(page, dialogo)
