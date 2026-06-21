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

def abrir_form_usuario_registrar(page: ft.Page):
    nombre = _campo_texto("Nombre", "Nombre")
    apellido = _campo_texto("Apellido", "Apellido")
    email = _campo_texto("Correo electrónico", "Correo electrónico")
    contrasena = _campo_texto("Contraseña", "Mínimo 6 caracteres", password=True)
    rol = _selector("Rol", ["Administrador", "Coordinador", "Brigadista"])
    id_brigada = _campo_numero("ID Brigada", "Número de brigada asignada")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Usuario registrado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("Nombre", nombre),
            ft.Container(height=12),
            _bloque_campo("Apellido", apellido),
            ft.Container(height=12),
            _bloque_campo("Correo electrónico", email),
            ft.Container(height=12),
            _bloque_campo("Contraseña", contrasena),
            ft.Container(height=12),
            _bloque_campo("Rol", rol),
            ft.Container(height=12),
            _bloque_campo("ID Brigada", id_brigada),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Registrar usuario", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_usuario_modificar(page: ft.Page):
    id_usuario = _campo_numero("ID Usuario", "Usuario a modificar")
    nombre = _campo_texto("Nombre", "")
    apellido = _campo_texto("Apellido", "")
    email = _campo_texto("Correo", "")
    rol = _selector("Rol", ["Administrador", "Coordinador", "Brigadista"])

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Usuario actualizado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Usuario", id_usuario),
            ft.Container(height=12),
            _bloque_campo("Nombre", nombre),
            ft.Container(height=12),
            _bloque_campo("Apellido", apellido),
            ft.Container(height=12),
            _bloque_campo("Correo", email),
            ft.Container(height=12),
            _bloque_campo("Rol", rol),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Modificar usuario", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_usuario_consultar(page: ft.Page):
    id_usuario = _campo_numero("ID Usuario", "Consultar por ID")
    resultado = ft.Text("Ingrese ID y pulse Buscar.", size=13, color=COLOR_TEXTO_SEC)

    def on_buscar(_):
        resultado.value = f"Consulta usuario ID {id_usuario.value or '(vacío)'} (pendiente conectar BD)."
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Usuario", id_usuario),
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
        title=ft.Text("Consultar usuario", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=420, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_TEXTO), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_form_usuario_eliminar(page: ft.Page):
    id_usuario = _campo_numero("ID Usuario", "Usuario a eliminar")

    def on_eliminar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Usuario eliminado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text("Confirme el ID del usuario a dar de baja.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            _bloque_campo("ID Usuario", id_usuario),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Eliminar usuario", contenido, on_guardar=on_eliminar, texto_guardar="Eliminar")
    _abrir_dialogo(page, dialogo)


# ---------- Brigadas (4.0) ----------


