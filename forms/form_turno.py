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

def abrir_form_turno(page: ft.Page):
    """Formulario de nuevo turno con DatePicker y TimePicker nativos + conexión a BD."""
    import database.crud_turno as crud_turno
    from datetime import datetime, date, time
    from database.crud_usuario import es_admin

    # Obtener el usuario_actual
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

    # ── Dropdown de brigadas reales ──
    brigadas_bd = _obtener_brigadas_form(page, brigada_rol_id)
    opciones_brigadas = [ft.dropdown.Option(str(bg["idBrigada"]), bg["nombre_brigada"]) for bg in brigadas_bd]

    brigada = ft.Dropdown(
        hint_text="Seleccione una brigada",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        options=opciones_brigadas,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        color=COLOR_TEXTO,
        content_padding=_CAMPO_PADDING,
    )

    # ── Estado interno para fecha y horas seleccionadas ──
    _fecha_sel = {"valor": None}    # date | None
    _hora_ini_sel = {"valor": None} # time | None
    _hora_fin_sel = {"valor": None} # time | None

    # ── Textos que muestran la selección ──
    texto_fecha = ft.Text("Seleccionar fecha…", size=14, color=COLOR_TEXTO_SEC, expand=True)
    texto_hora_ini = ft.Text("--:--", size=14, color=COLOR_TEXTO_SEC, expand=True)
    texto_hora_fin = ft.Text("--:--", size=14, color=COLOR_TEXTO_SEC, expand=True)

    # ── DatePicker (vía overlay para no reemplazar el diálogo del form) ──
    def _on_fecha_change(e):
        picked = e.control.value
        if picked:
            if isinstance(picked, datetime):
                picked = picked.date()
            _fecha_sel["valor"] = picked
            _MESES = {1:"Ene",2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",7:"Jul",8:"Ago",9:"Sep",10:"Oct",11:"Nov",12:"Dic"}
            texto_fecha.value = f"{picked.day:02d}/{_MESES.get(picked.month,'')}/{picked.year}"
            texto_fecha.color = COLOR_TEXTO
            page.update()

    date_picker = ft.DatePicker(
        first_date=date(2024, 1, 1),
        last_date=date(2030, 12, 31),
        on_change=_on_fecha_change,
    )

    # ── TimePicker — Hora Inicio (vía overlay) ──
    def _on_hora_ini_change(e):
        picked = e.control.value
        if picked:
            _hora_ini_sel["valor"] = picked
            texto_hora_ini.value = f"{picked.hour:02d}:{picked.minute:02d}"
            texto_hora_ini.color = COLOR_TEXTO
            page.update()

    time_picker_ini = ft.TimePicker(
        on_change=_on_hora_ini_change,
    )

    # ── TimePicker — Hora Fin (vía overlay) ──
    def _on_hora_fin_change(e):
        picked = e.control.value
        if picked:
            _hora_fin_sel["valor"] = picked
            texto_hora_fin.value = f"{picked.hour:02d}:{picked.minute:02d}"
            texto_hora_fin.color = COLOR_TEXTO
            page.update()

    time_picker_fin = ft.TimePicker(
        on_change=_on_hora_fin_change,
    )

    # Registrar pickers en overlay (para que no reemplacen el diálogo del formulario)
    page.overlay.append(date_picker)
    page.overlay.append(time_picker_ini)
    page.overlay.append(time_picker_fin)

    def _abrir_fecha(_):
        date_picker.open = True
        page.update()

    def _abrir_hora_ini(_):
        time_picker_ini.open = True
        page.update()

    def _abrir_hora_fin(_):
        time_picker_fin.open = True
        page.update()

    def _limpiar_overlay():
        """Remueve los pickers del overlay al cerrar el formulario."""
        for p in (date_picker, time_picker_ini, time_picker_fin):
            if p in page.overlay:
                page.overlay.remove(p)

    boton_fecha = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, size=20, color=COLOR_PRIMARIO),
                ft.Container(width=8),
                texto_fecha,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=20, color=COLOR_TEXTO_SEC),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(14, 12, 14, 12),
        border=ft.Border.all(1, COLOR_BORDE),
        border_radius=RADIO,
        bgcolor=COLOR_CARD,
        on_click=_abrir_fecha,
        ink=True,
    )

    boton_hora_ini = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, size=18, color=COLOR_PRIMARIO),
                ft.Container(width=6),
                texto_hora_ini,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=18, color=COLOR_TEXTO_SEC),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(14, 12, 14, 12),
        border=ft.Border.all(1, COLOR_BORDE),
        border_radius=RADIO,
        bgcolor=COLOR_CARD,
        on_click=_abrir_hora_ini,
        ink=True,
        expand=True,
    )

    boton_hora_fin = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, size=18, color=COLOR_PRIMARIO),
                ft.Container(width=6),
                texto_hora_fin,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=18, color=COLOR_TEXTO_SEC),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(14, 12, 14, 12),
        border=ft.Border.all(1, COLOR_BORDE),
        border_radius=RADIO,
        bgcolor=COLOR_CARD,
        on_click=_abrir_hora_fin,
        ink=True,
        expand=True,
    )

    # ── Fila de horas ──
    fila_horas = ft.Row(
        [
            ft.Column([ft.Text("Hora Inicio", size=14, weight="w500", color=COLOR_TEXTO), ft.Container(height=8), boton_hora_ini], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START, expand=True),
            ft.Container(width=16),
            ft.Column([ft.Text("Hora Fin", size=14, weight="w500", color=COLOR_TEXTO), ft.Container(height=8), boton_hora_fin], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START, expand=True),
        ],
        spacing=0,
    )

    ubicacion = ft.TextField(hint_text="Ubicación del turno", **_CAMPO_BASE)
    notas = ft.TextField(
        hint_text="Detalles adicionales del turno...",
        multiline=True,
        min_lines=3,
        max_lines=5,
        **_CAMPO_BASE,
    )

    contenido = ft.Column(
        [
            _campo_con_titulo("Brigada", brigada),
            _campo_con_titulo("Fecha", boton_fecha),
            fila_horas,
            ft.Container(height=16),
            _campo_con_titulo("Ubicación", ubicacion),
            _campo_con_titulo("Notas", notas, espaciado_abajo=0),
        ],
        spacing=0,
    )

    def on_crear(_):
        # ── Validaciones ──
        errores = []
        if not brigada.value:
            errores.append("Seleccione una brigada.")
        if not _fecha_sel["valor"]:
            errores.append("Seleccione una fecha.")
        if not _hora_ini_sel["valor"]:
            errores.append("Seleccione hora de inicio.")
        if not _hora_fin_sel["valor"]:
            errores.append("Seleccione hora de fin.")
        if _hora_ini_sel["valor"] and _hora_fin_sel["valor"]:
            if _hora_fin_sel["valor"] <= _hora_ini_sel["valor"]:
                errores.append("La hora de fin debe ser posterior a la hora de inicio.")

        if errores:
            page.snack_bar = ft.SnackBar(ft.Text(" | ".join(errores), color=COLOR_TEXTO), bgcolor=COLOR_CARD)
            page.snack_bar.open = True
            page.update()
            return

        # ── Insertar en BD ──
        fecha_str = _fecha_sel["valor"].strftime("%Y-%m-%d")
        hora_ini_str = f"{_hora_ini_sel['valor'].hour:02d}:{_hora_ini_sel['valor'].minute:02d}:00"
        hora_fin_str = f"{_hora_fin_sel['valor'].hour:02d}:{_hora_fin_sel['valor'].minute:02d}:00"

        try:
            lid = crud_turno.crear_turno(
                brigada_id=int(brigada.value),
                fecha=fecha_str,
                hora_inicio=hora_ini_str,
                hora_fin=hora_fin_str,
                ubicacion=(ubicacion.value or "").strip(),
                notas=(notas.value or "").strip(),
            )
            if lid:
                _limpiar_overlay()
                page.pop_dialog()
                page.snack_bar = ft.SnackBar(ft.Text("Turno creado con éxito ✓", color="white"), bgcolor=COLOR_PRIMARIO)
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error al guardar el turno en la base de datos.", color="white"), bgcolor="#ef4444")
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {err}", color="white"), bgcolor="#ef4444")

        page.snack_bar.open = True
        page.update()

    def _cerrar_form(e):
        _limpiar_overlay()
        _cerrar_dialogo(e.page if hasattr(e, 'page') else page)

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Row(
            [
                ft.Text("Nuevo Turno", size=18, weight="w600", color=COLOR_TEXTO),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.CLOSE, on_click=_cerrar_form),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=ANCHO_FORM,
            height=ALTURA_MAX_FORM,
            bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(content=ft.Text("Cancelar", color=COLOR_TEXTO), style=ft.ButtonStyle(color=COLOR_TEXTO), on_click=_cerrar_form),
            ft.FilledButton("Crear Turno", style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, color="white"), on_click=on_crear),
        ],
    )
    page.show_dialog(dialogo)


# ---------- Nuevo Reporte de Incidente (Figma) ----------
