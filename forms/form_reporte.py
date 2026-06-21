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

def abrir_form_reporte_registrar(page: ft.Page):
    contenido = _campo_texto("Contenido del reporte", "Redacte el reporte de impacto", multiline=True)
    id_actividad = _campo_numero("ID Actividad", "Actividad relacionada")
    id_usuario = _campo_numero("ID Usuario", "Usuario que genera el reporte")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Reporte registrado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    c = ft.Column(
        [
            _bloque_campo("Contenido del reporte", contenido),
            ft.Container(height=12),
            _bloque_campo("ID Actividad", id_actividad),
            ft.Container(height=12),
            _bloque_campo("ID Usuario", id_usuario),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Registrar reporte de impacto", c, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_reporte_modificar(page: ft.Page):
    id_reporte = _campo_numero("ID Reporte", "Reporte a modificar")
    contenido = _campo_texto("Contenido", "", multiline=True)

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Reporte actualizado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    c = ft.Column(
        [_bloque_campo("ID Reporte", id_reporte), ft.Container(height=12), _bloque_campo("Contenido", contenido)],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Modificar reporte", c, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_reporte_consultar(page: ft.Page):
    id_reporte = _campo_numero("ID Reporte", "Consultar por ID")
    resultado = ft.Text("Ingrese ID y pulse Buscar.", size=13, color=COLOR_TEXTO_SEC)

    def on_buscar(_):
        resultado.value = f"Consulta reporte ID {id_reporte.value or '(vacío)'} (pendiente conectar BD)."
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Reporte", id_reporte),
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
        title=ft.Text("Consultar reporte", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=420, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_TEXTO), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_form_reporte_eliminar(page: ft.Page):
    id_reporte = _campo_numero("ID Reporte", "Reporte a eliminar")

    def on_eliminar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Reporte eliminado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text("Confirme el ID del reporte a eliminar.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            _bloque_campo("ID Reporte", id_reporte),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Eliminar reporte", contenido, on_guardar=on_eliminar, texto_guardar="Eliminar")
    _abrir_dialogo(page, dialogo)


# ---------- Indicadores (7.0) ----------
# Indicador_ambiental: valor, tipo_indicador, unidad, Actividad_idActividad


def abrir_form_nuevo_reporte(page: ft.Page):
    """Cada campo con su título visible."""
    import database.crud_reporte as crud_reporte
    from database.crud_usuario import es_admin

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
    
    # Cargar brigadas reales
    brigadas_bd = _obtener_brigadas_form(page, brigada_rol_id)
    opciones_brigadas = []
    for bg in brigadas_bd:
        opciones_brigadas.append(ft.dropdown.Option(str(bg["idBrigada"]), bg["nombre_brigada"]))

    titulo_inc = ft.TextField(hint_text="Resumen breve del incidente", **_CAMPO_BASE)
    desc = ft.TextField(
        hint_text="Describe lo sucedido con detalle...",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        multiline=True,
        min_lines=3,
        max_lines=6,
        content_padding=ft.Padding(14, 20),
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        text_size=14,
        color=COLOR_TEXTO,
        cursor_color=COLOR_PRIMARIO,
    )
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
    ubicacion = ft.TextField(hint_text="Lugar donde ocurrió el incidente", **_CAMPO_BASE)
    severidad = ft.Dropdown(
        hint_text="Seleccione severidad",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        options=[
            ft.dropdown.Option("Baja"),
            ft.dropdown.Option("Media"),
            ft.dropdown.Option("Alta"),
        ],
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        color=COLOR_TEXTO,
        content_padding=_CAMPO_PADDING,
    )

    contenido = ft.Column(
        [
            _campo_con_titulo("Título del Incidente", titulo_inc),
            _campo_con_titulo("Descripción Detallada", desc),
            _campo_con_titulo("Brigada Involucrada", brigada),
            _campo_con_titulo("Ubicación", ubicacion),
            _campo_con_titulo("Severidad", severidad, espaciado_abajo=0),
        ],
        spacing=0,
    )

    def on_crear(_):
        if not all([titulo_inc.value, desc.value, brigada.value, ubicacion.value, severidad.value]):
            page.snack_bar = ft.SnackBar(ft.Text("Por favor complete todos los campos", color=COLOR_TEXTO), bgcolor=COLOR_CARD)
            page.snack_bar.open = True
            page.update()
            return

        crud_reporte.crear_reporte(
            titulo=titulo_inc.value, 
            descripcion=desc.value, 
            ubicacion=ubicacion.value, 
            prioridad=severidad.value, 
            brigada_id=int(brigada.value)
        )
        
        page.pop_dialog()
        page.snack_bar = ft.SnackBar(ft.Text("Reporte creado con éxito", color="white"), bgcolor=COLOR_PRIMARIO)
        page.snack_bar.open = True
        page.update()

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Nuevo Reporte de Incidente", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=ANCHO_FORM,
            height=ALTURA_MAX_FORM,
            bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(content=ft.Text("Cancelar", color=COLOR_TEXTO), style=ft.ButtonStyle(color=COLOR_TEXTO), on_click=lambda e: _cerrar_dialogo(e.page)),
            ft.FilledButton("Crear Reporte", style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, color="white"), on_click=on_crear),
        ],
    )
    page.show_dialog(dialogo)

# ==============================================================================
# FORMULARIOS: REPORTES DE ACTIVIDADES E IMPACTO
# ==============================================================================

def modal_nuevo_reporte_impacto(page: ft.Page, id_usuario_actual: int, on_success_callback=None):
    from database import crud_actividad, crud_reporte
    from database.crud_usuario import es_admin
    
    try:
        from components import resolver_contexto_filtrado
        ctx = resolver_contexto_filtrado(page)
        brigada_rol_id = ctx.get("brigada_rol_id")
    except Exception:
        brigada_rol_id = None
    
    # Brigadas reales
    brigadas_bd = _obtener_brigadas_form(page, brigada_rol_id)
    opciones_brigadas = [ft.dropdown.Option(str(bg["idBrigada"]), bg["nombre_brigada"]) for bg in brigadas_bd]

    brigada_dd = ft.Dropdown(
        hint_text="Seleccione la brigada",
        hint_style=ft.TextStyle(size=14, color=ft.Colors.with_opacity(0.7, COLOR_TEXTO)),
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        options=opciones_brigadas,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        color=COLOR_TEXTO,
        content_padding=_CAMPO_PADDING,
    )
    area_evaluada_tf = ft.TextField(
        hint_text="Ej. Patio central, Zona de recreo",
        **_CAMPO_BASE,
    )
    indicador_tf = ft.TextField(
        hint_text="Ej. Residuos recolectados, Horas de vigilancia",
        **_CAMPO_BASE,
    )
    # Valor y Unidad en fila
    valor_tf = ft.TextField(
        hint_text="Ej. 120",
        **_CAMPO_BASE,
    )
    unidad_tf = ft.TextField(
        hint_text="Ej. kg, horas, unidades",
        **_CAMPO_BASE,
    )
    descripcion_impacto = _campo_texto("Descripción", "Análisis del impacto observado...", multiline=True)
    descripcion_impacto.min_lines = 3
    descripcion_impacto.max_lines = 6
    descripcion_impacto.hint_style = ft.TextStyle(size=14, color=ft.Colors.with_opacity(0.7, COLOR_TEXTO))

    # Actividad asociada (opcional) - Solo completadas y de su brigada, excluyendo globales
    actividades = crud_actividad.listar_actividades(brigada_rol_id=brigada_rol_id, estado='Completada', excluir_globales=True)
    opciones_actividades = [ft.dropdown.Option("", "— Ninguna —")] + [
        ft.dropdown.Option(str(a["id"]), a["titulo"]) for a in actividades
    ]
    actividad_dd = ft.Dropdown(
        hint_text="Opcional",
        hint_style=ft.TextStyle(size=14, color=ft.Colors.with_opacity(0.7, COLOR_TEXTO)),
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        options=opciones_actividades,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        color=COLOR_TEXTO,
        content_padding=_CAMPO_PADDING,
    )

    fila_valor_unidad = ft.Row(
        [
            ft.Column(
                [ft.Text("Valor", size=14, weight="w500", color=COLOR_TEXTO), ft.Container(height=8), valor_tf],
                spacing=0, expand=True,
            ),
            ft.Container(width=16),
            ft.Column(
                [ft.Text("Unidad", size=14, weight="w500", color=COLOR_TEXTO), ft.Container(height=8), unidad_tf],
                spacing=0, expand=True,
            ),
        ],
        spacing=0,
    )

    archivos_seleccionados = []
    texto_archivos = ft.Text("Ningún archivo seleccionado", size=12, color=COLOR_TEXTO_SEC)
    
    def on_click_adjuntar(e):
        import tkinter as tk
        from tkinter import filedialog
        import os
        
        # Abrir diálogo nativo
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        rutas = filedialog.askopenfilenames(
            title="Seleccionar imágenes o videos",
            filetypes=[("Archivos multimedia", "*.png *.jpg *.jpeg *.mp4"), ("Todos los archivos", "*.*")]
        )
        root.destroy()
        
        if rutas:
            archivos_seleccionados.clear()
            archivos_seleccionados.extend(rutas)
            nombres = ", ".join([os.path.basename(r) for r in rutas])
            texto_archivos.value = f"Seleccionados: {nombres}"
        else:
            archivos_seleccionados.clear()
            texto_archivos.value = "Ningún archivo seleccionado"
        texto_archivos.update()
    
    boton_adjuntar = ft.ElevatedButton(
        "Adjuntar Imágenes/Videos",
        icon=ft.Icons.ATTACH_FILE,
        on_click=on_click_adjuntar,
        style=ft.ButtonStyle(color=COLOR_PRIMARIO, bgcolor=ft.Colors.with_opacity(0.1, COLOR_PRIMARIO))
    )

    contenido_modal = ft.Column(
        [
            _campo_con_titulo("Brigada", brigada_dd),
            _campo_con_titulo("Área Evaluada", area_evaluada_tf),
            _campo_con_titulo("Indicador", indicador_tf),
            fila_valor_unidad,
            ft.Container(height=16),
            _campo_con_titulo("Descripción del Impacto", descripcion_impacto),
            _campo_con_titulo("Actividad Asociada (opcional)", actividad_dd, espaciado_abajo=8),
            ft.Text("Archivos Adjuntos (opcional)", size=14, weight="w500", color=COLOR_TEXTO),
            ft.Container(height=4),
            ft.Row([boton_adjuntar, texto_archivos]),
            ft.Container(height=16),
        ],
        spacing=0,
    )

    def on_crear(e):
        if not brigada_dd.value or not area_evaluada_tf.value or not indicador_tf.value:
            setattr(page, 'snack_bar', ft.SnackBar(ft.Text("Brigada, área evaluada e indicador son obligatorios."), bgcolor=ft.Colors.RED))
            setattr(page.snack_bar, 'open', True)
            page.update()
            return

        # Resolver nombre de brigada a texto
        brigada_nombre = ""
        for bg in brigadas_bd:
            if str(bg["idBrigada"]) == brigada_dd.value:
                brigada_nombre = bg["nombre_brigada"]
                break

        act_id = None
        if actividad_dd.value and actividad_dd.value.strip():
            try:
                act_id = int(actividad_dd.value)
            except ValueError:
                act_id = None

        lid = crud_reporte.crear_reporte_impacto(
            usuario_id=id_usuario_actual,
            brigada=brigada_nombre,
            area_evaluada=(area_evaluada_tf.value or "").strip(),
            indicador=(indicador_tf.value or "").strip(),
            valor=(valor_tf.value or "").strip(),
            unidad=(unidad_tf.value or "").strip(),
            contenido=(descripcion_impacto.value or "").strip(),
            actividad_id=act_id,
        )
        
        if lid:
            import os, shutil
            from datetime import datetime
            
            # Guardar archivos
            if archivos_seleccionados:
                os.makedirs("uploads", exist_ok=True)
                for f_path in archivos_seleccionados:
                    if f_path:
                        nombre_original = os.path.basename(f_path)
                        ext = os.path.splitext(nombre_original)[1].lower()
                        tipo_archivo = "video" if ext == ".mp4" else "imagen"
                        nuevo_nombre = f"imp_{lid}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{nombre_original}"
                        ruta_dest = os.path.join("uploads", nuevo_nombre)
                        try:
                            shutil.copy(f_path, ruta_dest)
                            crud_reporte.guardar_media_reporte("impacto", lid, ruta_dest, tipo_archivo)
                        except Exception as ex:
                            print(f"Error copiando archivo {nombre_original}: {ex}")

            setattr(page, 'snack_bar', ft.SnackBar(ft.Text("Reporte de impacto guardado correctamente."), bgcolor=ft.Colors.GREEN))
            _cerrar_dialogo(page)
            if on_success_callback: on_success_callback()
        else:
            setattr(page, 'snack_bar', ft.SnackBar(ft.Text("Error en BD al guardar el reporte."), bgcolor=ft.Colors.RED))
        
        setattr(page.snack_bar, 'open', True)
        page.update()

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Nuevo Reporte de Impacto", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido_modal], scroll=ft.ScrollMode.AUTO, tight=True),
            width=ANCHO_FORM, height=ALTURA_MAX_FORM, bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: _cerrar_dialogo(page), style=ft.ButtonStyle(color=COLOR_TEXTO)),
            ft.FilledButton("Guardar Reporte", on_click=on_crear, style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, color="white")),
        ],
    )
    page.show_dialog(dialogo)


# ---------- Profesor — Registro y Asignación (v2) ----------


