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

def abrir_form_personal_registrar(page: ft.Page, on_success=None):
    """
    Formulario para que un Directivo registre un nuevo Profesor.
    Auto-inyecta institucion_id desde la sesión.
    Opcionalmente permite asignar brigada inmediatamente.
    """
    from database.crud_usuario import crear_usuario_institucional
    from database.crud_brigada import listar_brigadas_por_institucion

    usuario_actual = {}
    try:
        if getattr(page, "data", None) and isinstance(page.data.get("usuario_actual"), dict):
            usuario_actual = page.data["usuario_actual"]
        else:
            import json
            raw = page.client_storage.get("usuario_actual")
            usuario_actual = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except Exception:
        pass
    institucion_id = usuario_actual.get("institucion_id")
    if not institucion_id:
        page.snack_bar = ft.SnackBar(ft.Text("No se encontró la institución del usuario actual."), bgcolor="#ef4444")
        page.snack_bar.open = True
        page.update()
        return

    # Dropdown para rol en vez de RadioGroup para compatibilidad segura
    rol_radio = ft.Dropdown(
        options=[
            ft.dropdown.Option("Profesor", "Profesor"),
            ft.dropdown.Option("Estudiante", "Estudiante"),
        ],
        value="Profesor",
        **_DROPDOWN_BASE,
    )

    # Campos del formulario
    nombre = _campo_texto("Nombre *", "Nombre")
    apellido = _campo_texto("Apellido *", "Apellido")
    cedula = _campo_texto("Cédula", "V-12345678")
    email = _campo_texto("Correo electrónico *", "correo@ejemplo.com")
    usuario_str = _campo_texto("Usuario *", "nombre_usuario")
    contrasena = _campo_texto("Contraseña *", "Mínimo 6 caracteres", password=True)
    confirmar = _campo_texto("Confirmar contraseña *", "", password=True)

    # Dropdown de brigadas sin profesor
    try:
        brigadas_disp = listar_brigadas_por_institucion(institucion_id, solo_sin_profesor=True)
    except Exception:
        brigadas_disp = []
    opciones_brigada = [ft.dropdown.Option("", "Seleccione una brigada")]
    for b in brigadas_disp:
        opciones_brigada.append(ft.dropdown.Option(str(b["idBrigada"]), b.get("nombre_brigada", f"Brigada {b['idBrigada']}")))
    dropdown_brigada = ft.Dropdown(
        hint_text="Asignar a brigada",
        options=opciones_brigada,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        text_size=14,
        color=COLOR_TEXTO,
        content_padding=ft.Padding(14, 14),
        border_radius=RADIO,
        hint_style=ft.TextStyle(size=14, color=ft.Colors.GREY_700),
    )
    container_brigada = _campo_con_titulo("Asignar a brigada *", dropdown_brigada)

    def _on_rol_change(e):
        if rol_radio.value == "Estudiante":
            container_brigada.visible = False
            dropdown_brigada.value = None
        else:
            container_brigada.visible = True
        page.update()

    rol_radio.on_change = _on_rol_change

    def on_crear(_):
        btn_registrar.disabled = True
        btn_registrar.text = "Registrando..."
        page.update()

        def _error(mensaje: str):
            page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor="#ef4444")
            page.snack_bar.open = True
            btn_registrar.disabled = False
            btn_registrar.text = "Registrar"
            page.update()

        try:
            # Validaciones
            if not nombre.value or not nombre.value.strip():
                _error("El nombre es obligatorio.")
                return
            if not apellido.value or not apellido.value.strip():
                _error("El apellido es obligatorio.")
                return
            if not email.value or not email.value.strip():
                _error("El correo electronico es obligatorio.")
                return
            if not usuario_str.value or not usuario_str.value.strip():
                _error("El usuario es obligatorio.")
                return
            if not contrasena.value or len(contrasena.value) < 6:
                _error("La contrasena debe tener al menos 6 caracteres.")
                return
            if contrasena.value != confirmar.value:
                _error("Las contrasenas no coinciden.")
                return

            email_val = email.value.strip().lower()
            usuario_val = usuario_str.value.strip().lower()
            cedula_val = (cedula.value or "").strip() or None

            if email_ya_existe(email_val):
                _error("Ese correo ya esta registrado.")
                return
            if usuario_ya_existe(usuario_val):
                _error("Ese usuario ya esta registrado.")
                return
            if cedula_val and cedula_ya_existe(cedula_val):
                _error("Esa cedula ya esta registrada.")
                return

            brigada_id = None
            if dropdown_brigada.value and dropdown_brigada.value.strip():
                try:
                    brigada_id = int(dropdown_brigada.value)
                except (ValueError, TypeError):
                    brigada_id = None
            if rol_radio.value == "Profesor" and not brigada_id:
                if not brigadas_disp:
                    _error("No hay brigadas disponibles sin profesor responsable en esta institucion.")
                else:
                    _error("Seleccione una brigada para asignar al profesor.")
                return

            crear_usuario_institucional(
                nombre=nombre.value.strip(),
                apellido=apellido.value.strip(),
                email=email_val,
                contrasena_plana=contrasena.value,
                usuario_str=usuario_val,
                cedula=cedula_val,
                institucion_id=institucion_id,
                brigada_id=brigada_id,
                rol=rol_radio.value,
            )
            _cerrar_dialogo(page)
            page.snack_bar = ft.SnackBar(ft.Text(f"{rol_radio.value} registrado correctamente."), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success:
                on_success()
            page.update()
        except Exception as ex:
            _error(f"Error al registrar {rol_radio.value.lower()}: {ex}")

    contenido = ft.Container(
        content=ft.Column(
            [
                _campo_con_titulo("Rol *", rol_radio),
                _campo_con_titulo("Nombre *", nombre),
                _campo_con_titulo("Apellido *", apellido),
                _campo_con_titulo("Cédula", cedula),
                _campo_con_titulo("Correo electrónico *", email),
                _campo_con_titulo("Usuario *", usuario_str),
                _campo_con_titulo("Contraseña *", contrasena),
                _campo_con_titulo("Confirmar contraseña *", confirmar),
                ft.Container(height=8),
                container_brigada,
            ],
            spacing=0,
        ),
        padding=PADDING,
        width=ANCHO_FORM,
    )

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Registrar Personal/Estudiante", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=ANCHO_FORM, height=ALTURA_MAX_FORM, bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: _cerrar_dialogo(page), style=ft.ButtonStyle(color=COLOR_TEXTO)),
            btn_registrar := ft.FilledButton("Registrar", on_click=on_crear, style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, color="white")),
        ],
    )
    _abrir_dialogo(page, dialogo)


