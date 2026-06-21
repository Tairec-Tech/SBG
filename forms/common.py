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


def _obtener_brigadas_form(page, brigada_rol_id=None):
    from components import resolver_contexto_filtrado
    from database.crud_brigada import listar_brigadas
    ctx = resolver_contexto_filtrado(page)
    if brigada_rol_id is not None:
        return listar_brigadas(brigada_rol_id=brigada_rol_id)
    if ctx["modo"] == "institucional":
        return listar_brigadas(institucion_id=ctx["institucion_id"])
    elif ctx["modo"] == "brigada":
        return listar_brigadas(brigada_rol_id=ctx["brigada_rol_id"])
    return []


def _etiqueta(texto: str) -> ft.Control:
    return ft.Text(texto, size=13, weight="w500", color=COLOR_TEXTO_SEC)


def _campo_texto(label: str, hint: str = "", password: bool = False, multiline: bool = False, value: str = "") -> ft.TextField:
    return ft.TextField(
        hint_text=hint,
        value=value or None,
        password=password,
        multiline=multiline,
        min_lines=1,
        max_lines=4 if multiline else 1,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        text_size=14,
        color=COLOR_TEXTO,
        cursor_color=COLOR_PRIMARIO,
        content_padding=ft.Padding(14, 14),
        border_radius=RADIO,
        hint_style=ft.TextStyle(size=14, color=ft.Colors.GREY_700),
    )


def _campo_numero(label: str, hint: str = "", value: str = "") -> ft.TextField:
    return ft.TextField(
        hint_text=hint,
        value=value or None,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        text_size=14,
        color=COLOR_TEXTO,
        cursor_color=COLOR_PRIMARIO,
        content_padding=ft.Padding(14, 14),
        border_radius=RADIO,
        hint_style=ft.TextStyle(size=14, color=ft.Colors.GREY_700),
    )


def _selector(label: str, opciones: list, value: str = "") -> ft.Dropdown:
    return ft.Dropdown(
        hint_text=label,
        options=[ft.dropdown.Option(str(o)) for o in opciones],
        value=value or (opciones[0] if opciones else None),
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        text_size=14,
        color=COLOR_TEXTO,
        content_padding=ft.Padding(14, 14),
        border_radius=RADIO,
        hint_style=ft.TextStyle(size=14, color=ft.Colors.GREY_700),
    )


def _bloque_campo(label: str, control: ft.Control) -> ft.Column:
    return ft.Column(
        [ft.Container(content=_etiqueta(label), padding=ft.Padding(0, 0, 0, 6)), control],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=4,
    )


def _campo_con_titulo(titulo: str, control: ft.Control, espaciado_abajo: int = 16) -> ft.Column:
    """Título visible sobre el control; se usa en todos los formularios tipo Figma."""
    return ft.Column(
        [
            ft.Text(titulo, size=14, weight="w500", color=COLOR_TEXTO),
            ft.Container(height=8),
            control,
            ft.Container(height=espaciado_abajo),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=0,
    )


def _cerrar_dialogo(page: ft.Page, _dialogo=None):
    """Cierra el diálogo activo usando la API de Flet (pop_dialog)."""
    page.pop_dialog()


def _on_cancelar(e: ft.ControlEvent, _dialogo=None):
    """Callback del botón Cancelar: cierra el diálogo activo."""
    _cerrar_dialogo(e.page)


def _dialogo_formulario(
    page: ft.Page,
    titulo: str,
    contenido: ft.Control,
    ancho: float = None,
    on_guardar=None,
    texto_guardar: str = "Guardar",
    on_cancelar=None,
) -> ft.AlertDialog:
    """Crea un AlertDialog con contenido de formulario y botones Guardar/Cancelar."""
    w = ancho if ancho is not None else ANCHO_FORM
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text(titulo, size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=w,
            bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(
                content=ft.Text("Cancelar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500),
                style=ft.ButtonStyle(color=COLOR_TEXTO),
                on_click=lambda e: _on_cancelar(e),
            ),
            ft.FilledButton(
                texto_guardar,
                style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, color="white"),
                on_click=lambda e: on_guardar(e) if on_guardar else None,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    return dialogo


def _abrir_dialogo(page: ft.Page, dialogo: ft.AlertDialog):
    """Abre el diálogo usando la API de Flet (show_dialog)."""
    page.show_dialog(dialogo)


# ---------- Instituciones (2.0) ----------
# Institucion_Educativa: nombre_institucion, direccion, telefono


