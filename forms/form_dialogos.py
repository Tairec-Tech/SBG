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

def abrir_dialogo_acerca_de(page: ft.Page):
    contenido = ft.Column(
        [
            ft.Text("Sistema de Brigadas Escolares (SBE)", size=16, weight="w600", color=COLOR_TEXTO),
            ft.Container(height=8),
            ft.Text("Municipio Maracaibo — Gestión de brigadas escolares.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=12),
            ft.Text("Versión 1.0", size=12, color=COLOR_TEXTO_SEC),
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Acerca de", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=380, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_TEXTO), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_dialogo_manual(page: ft.Page):
    contenido = ft.Column(
        [
            ft.Text("Manual de usuario y documentación del sistema.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=12),
            ft.Text("Consulte la documentación incluida en el proyecto o con el administrador.", size=13, color=COLOR_TEXTO_SEC),
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Manual de usuario", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=400, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_TEXTO), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_dialogo_legal(page: ft.Page):
    contenido = ft.Column(
        [
            ft.Text("Términos de uso, licencias y créditos del sistema.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=12),
            ft.Text("SBE — Uso institucional. Consulte con la entidad responsable.", size=13, color=COLOR_TEXTO_SEC),
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Información legal", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=400, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_TEXTO), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_dialogo_importar_bd(page: ft.Page):
    contenido = ft.Column(
        [
            ft.Text("Importar o restaurar la base de datos desde un archivo de respaldo.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            ft.Text("Funcionalidad de respaldo/restauración (pendiente conectar con BD).", size=12, color=COLOR_TEXTO_SEC),
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Importar / restaurar BD", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=400, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_TEXTO), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


# ---------- Nuevo Turno (Figma) ----------
