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

def abrir_form_brigadista_registrar(page: ft.Page, on_success=None):
    """Registrar alumno (brigadista). Los alumnos no usan el programa; solo se registran aquí. Cédula obligatoria."""
    nombre = ft.TextField(hint_text="Nombre", **_CAMPO_BASE)
    apellido = ft.TextField(hint_text="Apellido", **_CAMPO_BASE)
    cedula = ft.TextField(hint_text="Cédula (obligatoria)", **_CAMPO_BASE)
    rol_brigadista = ft.Dropdown(
        hint_text="Rol en la brigada",
        options=[
            ft.dropdown.Option("Brigadista Jefe", "Jefe de Brigada"),
            ft.dropdown.Option("Brigadista", "Brigadista"),
        ],
        value="Brigadista",
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        text_size=14,
        color=COLOR_TEXTO,
        content_padding=_CAMPO_PADDING,
    )
    import json
    try:
        user_raw = page.client_storage.get("usuario_actual")
        usuario_actual = page.data.get("usuario_actual") if getattr(page, "data", None) and getattr(page.data, "get", None) else None
        if not usuario_actual and user_raw:
            usuario_actual = json.loads(user_raw) if isinstance(user_raw, str) else (user_raw or {})
    except Exception:
        usuario_actual = {}
        
    usuario_actual = usuario_actual or {}
    rol_actual = usuario_actual.get("rol", "")
    brigada_rol_id = usuario_actual.get("Brigada_idBrigada") if not es_admin(rol_actual) else None

    brigadas_opciones = []
    try:
        for b in _obtener_brigadas_form(page, brigada_rol_id):
            brigadas_opciones.append(ft.dropdown.Option(str(b["idBrigada"]), b["nombre_brigada"] or f"Brigada {b['idBrigada']}"))
    except Exception:
        pass
    brigada = ft.Dropdown(
        hint_text="Seleccione una brigada",
        options=brigadas_opciones,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        text_size=14,
        color=COLOR_TEXTO,
        content_padding=_CAMPO_PADDING,
    )

    contenido = ft.Column(
        [
            ft.Text("Los alumnos no inician sesión en el sistema; solo se registran desde aquí.", size=12, color=COLOR_TEXTO_SEC),
            ft.Container(height=12),
            _campo_con_titulo("Nombre *", nombre),
            _campo_con_titulo("Apellido *", apellido),
            _campo_con_titulo("Cédula *", cedula),
            _campo_con_titulo("Rol en la Brigada", rol_brigadista),
            _campo_con_titulo("Brigada *", brigada, espaciado_abajo=0),
        ],
        spacing=0,
    )

    def on_agregar(_):
        nom = (nombre.value or "").strip()
        ape = (apellido.value or "").strip()
        cedula_val = (cedula.value or "").strip()
        brigada_id_val = brigada.value
        if not nom:
            page.snack_bar = ft.SnackBar(ft.Text("El nombre es obligatorio"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        if not ape:
            page.snack_bar = ft.SnackBar(ft.Text("El apellido es obligatorio"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        if not cedula_val:
            page.snack_bar = ft.SnackBar(ft.Text("La cédula es obligatoria"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        if not brigada_id_val:
            page.snack_bar = ft.SnackBar(ft.Text("Seleccione una brigada"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        if cedula_ya_existe(cedula_val):
            page.snack_bar = ft.SnackBar(ft.Text("Ya existe un brigadista con esa cédula"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        try:
            rol_seleccionado = rol_brigadista.value or "Brigadista"
            # Alumnos no usan el programa: email y contraseña internos
            email_alumno = f"{cedula_val}@alumno.local"
            if email_ya_existe(email_alumno):
                email_alumno = f"{cedula_val}_{id(page)}@alumno.local"
            crear_usuario(
                nombre=nom,
                apellido=ape,
                email=email_alumno,
                contrasena_plana="alumno123",
                rol=rol_seleccionado,
                brigada_id=int(brigada_id_val),
                cedula=cedula_val,
            )
            _cerrar_dialogo(page)
            page.snack_bar = ft.SnackBar(ft.Text("¡Alumno (brigadista) registrado correctamente!"), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success:
                on_success()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="#ef4444")
            page.snack_bar.open = True
        page.update()

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Registrar alumno (brigadista)", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=ANCHO_FORM,
            bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(content=ft.Text("Cancelar", color=COLOR_TEXTO), style=ft.ButtonStyle(color=COLOR_TEXTO), on_click=lambda e: _cerrar_dialogo(e.page)),
            ft.FilledButton("Agregar alumno", style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, color="white"), on_click=on_agregar),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.show_dialog(dialogo)


def abrir_form_brigadista_modificar(page: ft.Page, brigadista=None, on_success=None):
    """Abre el formulario para editar un brigadista (Usuario). Precarga datos y actualiza en BD (incl. cédula)."""
    if not brigadista:
        page.snack_bar = ft.SnackBar(ft.Text("Error: no se pasó el brigadista"))
        page.snack_bar.open = True
        page.update()
        return
    id_val = brigadista.get("idUsuario")
    nombre = ft.TextField(label="Nombre", value=brigadista.get("nombre") or "", **_CAMPO_BASE)
    apellido = ft.TextField(label="Apellido", value=brigadista.get("apellido") or "", **_CAMPO_BASE)
    cedula = ft.TextField(label="Cédula", value=brigadista.get("cedula") or "", **_CAMPO_BASE)
    correo = ft.TextField(label="Correo electrónico", value=brigadista.get("email") or "", **_CAMPO_BASE)
    rol = ft.Dropdown(
        label="Rol",
        value=brigadista.get("rol") or "Brigadista",
        options=[
            ft.dropdown.Option("Brigadista Jefe", "Jefe de Brigada"),
            ft.dropdown.Option("Brigadista", "Brigadista"),
            ft.dropdown.Option("Profesor", "Profesor"),
            ft.dropdown.Option("Coordinador", "Coordinador"),
            ft.dropdown.Option("Directivo", "Directivo"),
        ],
        **_DROPDOWN_BASE,
    )
    import json
    try:
        user_raw = page.client_storage.get("usuario_actual")
        usuario_actual = page.data.get("usuario_actual") if getattr(page, "data", None) and getattr(page.data, "get", None) else None
        if not usuario_actual and user_raw:
            usuario_actual = json.loads(user_raw) if isinstance(user_raw, str) else (user_raw or {})
    except Exception:
        usuario_actual = {}
        
    usuario_actual = usuario_actual or {}
    rol_actual = usuario_actual.get("rol", "")
    brigada_rol_id = usuario_actual.get("Brigada_idBrigada") if not es_admin(rol_actual) else None

    brigadas_opciones = []
    try:
        for b in _obtener_brigadas_form(page, brigada_rol_id):
            brigadas_opciones.append(ft.dropdown.Option(str(b["idBrigada"]), b["nombre_brigada"] or f"Brigada {b['idBrigada']}"))
    except Exception:
        pass
    brigada = ft.Dropdown(
        label="Brigada",
        value=str(brigadista.get("Brigada_idBrigada") or ""),
        options=brigadas_opciones,
        **_DROPDOWN_BASE,
    )

    def on_guardar(_):
        nom = (nombre.value or "").strip()
        ape = (apellido.value or "").strip()
        cedula_val = (cedula.value or "").strip()
        email_val = (correo.value or "").strip().lower()
        if not nom:
            page.snack_bar = ft.SnackBar(ft.Text("El nombre es obligatorio"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        if not email_val:
            page.snack_bar = ft.SnackBar(ft.Text("El correo es obligatorio"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        brigada_id_val = brigada.value
        if not brigada_id_val:
            page.snack_bar = ft.SnackBar(ft.Text("Seleccione una brigada"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        if cedula_val:
            otro_id = obtener_id_usuario_por_cedula(cedula_val)
            if otro_id is not None and otro_id != id_val:
                page.snack_bar = ft.SnackBar(ft.Text("Ya existe otro brigadista con esa cédula"), bgcolor="#ef4444")
                page.snack_bar.open = True
                page.update()
                return
        try:
            actualizar_usuario(
                id_usuario=id_val,
                nombre=nom,
                apellido=ape,
                email=email_val,
                rol=(rol.value or "Brigadista"),
                brigada_id=int(brigada_id_val),
                cedula=cedula_val or None,
            )
            _cerrar_dialogo(page)
            page.snack_bar = ft.SnackBar(ft.Text("¡Brigadista actualizado correctamente!"), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success:
                on_success()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="#ef4444")
            page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [ft.Text(f"ID: {id_val}", size=13, color=COLOR_TEXTO_SEC), ft.Container(height=12), nombre, apellido, cedula, correo, rol, brigada],
        spacing=12,
    )
    dialogo = _dialogo_formulario(page, "Modificar brigadista", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_brigadista_eliminar(page: ft.Page, brigadista=None, on_success=None):
    """Confirmación para eliminar un brigadista (Usuario)."""
    if not brigadista:
        page.snack_bar = ft.SnackBar(ft.Text("Error: no se pasó el brigadista"))
        page.snack_bar.open = True
        page.update()
        return
    id_val = brigadista.get("idUsuario")
    nombre_completo = f"{brigadista.get('nombre') or ''} {brigadista.get('apellido') or ''}".strip() or brigadista.get("email") or "este usuario"

    def on_eliminar(_):
        err = eliminar_usuario(id_val)
        if err:
            page.snack_bar = ft.SnackBar(ft.Text(err))
            page.snack_bar.open = True
            page.update()
            return
        _cerrar_dialogo(page)
        page.snack_bar = ft.SnackBar(ft.Text("Brigadista eliminado correctamente"), bgcolor="#22c55e")
        page.snack_bar.open = True
        if on_success:
            on_success()
        page.update()

    contenido = ft.Column(
        [
            ft.Text(f"¿Eliminar a {nombre_completo} (ID {id_val})? Esta acción no se puede deshacer.", size=14, color=COLOR_TEXTO),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Eliminar brigadista", contenido, on_guardar=on_eliminar, texto_guardar="Eliminar")
    _abrir_dialogo(page, dialogo)


