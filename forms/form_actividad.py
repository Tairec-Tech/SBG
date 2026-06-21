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

def abrir_form_actividad_registrar(page: ft.Page):
    titulo = _campo_texto("Título", "Nombre de la actividad")
    descripcion = _campo_texto("Descripción", "Detalle", multiline=True)
    estado = _selector("Estado", ["Planificada", "En curso", "Finalizada"])
    fecha_inicio = _campo_texto("Fecha inicio", "YYYY-MM-DD")
    fecha_fin = _campo_texto("Fecha fin", "YYYY-MM-DD")
    id_brigada = _campo_numero("ID Brigada", "Brigada responsable")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Actividad registrada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("Título", titulo),
            ft.Container(height=12),
            _bloque_campo("Descripción", descripcion),
            ft.Container(height=12),
            _bloque_campo("Estado", estado),
            ft.Container(height=12),
            _bloque_campo("Fecha inicio", fecha_inicio),
            ft.Container(height=12),
            _bloque_campo("Fecha fin", fecha_fin),
            ft.Container(height=12),
            _bloque_campo("ID Brigada", id_brigada),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Registrar actividad", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_actividad_modificar(page: ft.Page):
    id_act = _campo_numero("ID Actividad", "Actividad a modificar")
    titulo = _campo_texto("Título", "")
    descripcion = _campo_texto("Descripción", "", multiline=True)
    estado = _selector("Estado", ["Planificada", "En curso", "Finalizada"])
    fecha_inicio = _campo_texto("Fecha inicio", "YYYY-MM-DD")
    fecha_fin = _campo_texto("Fecha fin", "YYYY-MM-DD")
    id_brigada = _campo_numero("ID Brigada", "")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Actividad actualizada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Actividad", id_act),
            ft.Container(height=12),
            _bloque_campo("Título", titulo),
            ft.Container(height=12),
            _bloque_campo("Descripción", descripcion),
            ft.Container(height=12),
            _bloque_campo("Estado", estado),
            ft.Container(height=12),
            _bloque_campo("Fecha inicio", fecha_inicio),
            ft.Container(height=12),
            _bloque_campo("Fecha fin", fecha_fin),
            ft.Container(height=12),
            _bloque_campo("ID Brigada", id_brigada),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Modificar actividad", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_actividad_consultar(page: ft.Page):
    id_act = _campo_numero("ID Actividad", "Consultar por ID")
    resultado = ft.Text("Ingrese ID y pulse Buscar.", size=13, color=COLOR_TEXTO_SEC)

    def on_buscar(_):
        resultado.value = f"Consulta actividad ID {id_act.value or '(vacío)'} (pendiente conectar BD)."
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Actividad", id_act),
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
        title=ft.Text("Consultar actividad", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=420, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_TEXTO), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_form_actividad_eliminar(page: ft.Page):
    id_act = _campo_numero("ID Actividad", "Actividad a eliminar")

    def on_eliminar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Actividad eliminada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text("Eliminar una actividad puede afectar indicadores y reportes asociados.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            _bloque_campo("ID Actividad", id_act),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Eliminar actividad", contenido, on_guardar=on_eliminar, texto_guardar="Eliminar")
    _abrir_dialogo(page, dialogo)


def abrir_form_actividad_planificar(page: ft.Page):
    id_act = _campo_numero("ID Actividad", "Actividad a planificar")
    id_brigada = _campo_numero("ID Brigada", "Brigada responsable")
    fecha_inicio = _campo_texto("Fecha inicio", "YYYY-MM-DD")
    fecha_fin = _campo_texto("Fecha fin", "YYYY-MM-DD")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Planificación registrada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Actividad", id_act),
            ft.Container(height=12),
            _bloque_campo("ID Brigada", id_brigada),
            ft.Container(height=12),
            _bloque_campo("Fecha inicio", fecha_inicio),
            ft.Container(height=12),
            _bloque_campo("Fecha fin", fecha_fin),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Planificar actividad", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


# ---------- Reportes (6.0) ----------
# Reporte_de_impacto: contenido, fecha_generacion, Actividad_idActividad, Usuario_idUsuario


def modal_nuevo_reporte_actividad(page: ft.Page, id_usuario_actual: int, on_success_callback=None):
    from database import crud_actividad, crud_reporte
    from database.crud_usuario import es_admin
    import json
    
    try:
        from components import resolver_contexto_filtrado
        ctx = resolver_contexto_filtrado(page)
        brigada_rol_id = ctx.get("brigada_rol_id")
    except Exception:
        brigada_rol_id = None
    
    # Obtener actividades para el dropdown (solo completadas, propias de la brigada, y excluyendo globales)
    actividades = crud_actividad.listar_actividades(brigada_rol_id=brigada_rol_id, estado='Completada', excluir_globales=True)
    opciones_actividades = [ft.dropdown.Option(str(a["id"]), a["titulo"]) for a in actividades]
    
    actividad_dd = ft.Dropdown(
        hint_text="Seleccione la actividad",
        hint_style=ft.TextStyle(size=14, color=ft.Colors.with_opacity(0.7, COLOR_TEXTO)),
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        options=opciones_actividades,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        color=COLOR_TEXTO,
        content_padding=_CAMPO_PADDING,
    )
    participantes_tf = ft.TextField(
        hint_text="Ej. 25 estudiantes, 2 profesores",
        **_CAMPO_BASE,
    )
    observaciones = _campo_texto("Observaciones", "Resumen de lo ocurrido durante la actividad...", multiline=True)
    observaciones.min_lines = 3
    observaciones.max_lines = 5
    observaciones.hint_style = ft.TextStyle(size=14, color=ft.Colors.with_opacity(0.7, COLOR_TEXTO))
    
    resultado = _campo_texto("Estado Final", "Ej. Completado con éxito", multiline=True)
    resultado.min_lines = 2
    resultado.max_lines = 3
    resultado.hint_style = ft.TextStyle(size=14, color=ft.Colors.with_opacity(0.7, COLOR_TEXTO))
    
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
    
    contenido = ft.Column(
        [
            _campo_con_titulo("Actividad Realizada", actividad_dd),
            _campo_con_titulo("Participantes", participantes_tf),
            _campo_con_titulo("Observaciones", observaciones),
            _campo_con_titulo("Estado Final (Resultado)", resultado, espaciado_abajo=8),
            ft.Text("Archivos Adjuntos (opcional)", size=14, weight="w500", color=COLOR_TEXTO),
            ft.Container(height=4),
            ft.Row([boton_adjuntar, texto_archivos]),
            ft.Container(height=16),
        ],
        spacing=0,
    )

    def on_crear(e):
        if not actividad_dd.value or not observaciones.value or not resultado.value:
            setattr(page, 'snack_bar', ft.SnackBar(ft.Text("Actividad, observaciones y estado final son obligatorios."), bgcolor=ft.Colors.RED))
            setattr(page.snack_bar, 'open', True)
            page.update()
            return
            
        lid = crud_reporte.crear_reporte_actividad(
            resumen=observaciones.value,
            resultado=resultado.value,
            actividad_id=int(actividad_dd.value),
            usuario_id=id_usuario_actual,
            participantes=(participantes_tf.value or "").strip(),
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
                        nuevo_nombre = f"act_{lid}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{nombre_original}"
                        ruta_dest = os.path.join("uploads", nuevo_nombre)
                        try:
                            shutil.copy(f_path, ruta_dest)
                            crud_reporte.guardar_media_reporte("actividad", lid, ruta_dest, tipo_archivo)
                        except Exception as ex:
                            print(f"Error copiando archivo {nombre_original}: {ex}")

            setattr(page, 'snack_bar', ft.SnackBar(ft.Text("Reporte de actividad guardado correctamente."), bgcolor=ft.Colors.GREEN))
            _cerrar_dialogo(page)
            if on_success_callback: on_success_callback()
        else:
            setattr(page, 'snack_bar', ft.SnackBar(ft.Text("Error en BD al guardar el reporte."), bgcolor=ft.Colors.RED))
        
        setattr(page.snack_bar, 'open', True)
        page.update()

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Nuevo Reporte de Actividad", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=ANCHO_FORM, height=ALTURA_MAX_FORM, bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: _cerrar_dialogo(page), style=ft.ButtonStyle(color=COLOR_TEXTO)),
            ft.FilledButton("Guardar Reporte", on_click=on_crear, style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, color="white")),
        ],
    )
    page.show_dialog(dialogo)

