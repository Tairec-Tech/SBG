"""Pantalla de gestión de Actividades — SBE.
Funcionalidad:
- Por defecto muestra solo las actividades del profesor actual.
- Toggle para ver las actividades de otros (solo lectura).
- Acciones sobre las propias: completar, editar, eliminar.
- Admin puede operar sobre todas.
"""
import flet as ft
from datetime import date
from theme import (
    COLOR_FONDO_VERDE,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_PRIMARIO,
    COLOR_CARD,
    COLOR_BORDE,
    RADIO,
    get_sombra_suave,
)
from components import (
    card_principal,
    titulo_pagina,
    boton_primario,
)
from forms import (
    _campo_texto,
    _campo_con_titulo,
    _cerrar_dialogo,
    _abrir_dialogo,
)
import database.crud_actividad as crud_act
import database.crud_brigada as crud_brigada
from database.crud_usuario import es_admin, es_profesor
import json


def _obtener_usuario_actual(page: ft.Page) -> dict:
    """Obtiene el usuario actual desde page.data (login) o client_storage."""
    try:
        if getattr(page, "data", None) and isinstance(page.data.get("usuario_actual"), dict):
            return page.data["usuario_actual"]
        usuario_json = page.client_storage.get("usuario_actual")
        if usuario_json:
            return json.loads(usuario_json) if isinstance(usuario_json, str) else (usuario_json or {})
    except Exception:
        pass
    return {}


# ─── Modal: Crear / Editar actividad ─────────────────────────────────

def _abrir_modal_actividad(page: ft.Page, on_success=None, usuario_actual=None, actividad=None):
    """
    Abre un diálogo para crear o editar una actividad planificada.
    - Creación: campos principales + sección avanzada colapsable.
    - Edición: precarga datos; muestra Resultado Obtenido solo si estado es Completada.
    """
    usuario_actual = usuario_actual or {}
    rol = usuario_actual.get("rol", "")
    user_id = usuario_actual.get("id")
    editando = actividad is not None
    from datetime import datetime
    import util_json_plan
    from components import resolver_contexto_filtrado

    desc_raw = actividad.get("descripcion", "") if editando else ""
    plan_data = util_json_plan.deserializar_plan(desc_raw)

    # ── Estilos con hint_style corregido ──
    _CAMPO = dict(
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        text_size=14,
        color=COLOR_TEXTO,
        cursor_color=COLOR_PRIMARIO,
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        label_style=ft.TextStyle(size=13, color=COLOR_TEXTO_SEC),
    )
    _DROPDOWN = dict(
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        text_size=14,
        color=COLOR_TEXTO,
        border_radius=RADIO,
        dense=True,
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        label_style=ft.TextStyle(size=13, color=COLOR_TEXTO_SEC),
    )

    # ── CAMPOS PRINCIPALES ──
    titulo_campo = ft.TextField(
        hint_text="Nombre de la actividad",
        value=actividad.get("titulo", "") if editando else "",
        content_padding=ft.Padding(14, 14), **_CAMPO,
    )
    objetivo_campo = ft.TextField(
        hint_text="Objetivo central o plan de acción",
        value=plan_data.get("objetivo_plan", ""),
        multiline=True, min_lines=2, max_lines=4,
        content_padding=ft.Padding(14, 14), **_CAMPO,
    )

    # ── CAMPOS AVANZADOS ──
    momento_escolar_campo = ft.Dropdown(
        options=[ft.dropdown.Option(x) for x in ["Ordinario", "Regreso a Clases", "Cierre de Proyecto", "Semana Aniversario", "Vacaciones"]],
        value=plan_data.get("momento_escolar") or "Ordinario",
        content_padding=ft.Padding(12, 14), **_DROPDOWN,
    )
    origen_campo = ft.Dropdown(
        options=[ft.dropdown.Option(x) for x in ["Cronograma", "Reactivo", "Proactivo"]],
        value=plan_data.get("origen_actividad") or "Cronograma",
        content_padding=ft.Padding(12, 14), **_DROPDOWN,
    )
    efemeride_campo = ft.TextField(
        hint_text="Efeméride (si aplica)",
        value=plan_data.get("efemeride", ""),
        content_padding=ft.Padding(14, 14), **_CAMPO,
    )
    nivel_educativo_campo = ft.Dropdown(
        options=[ft.dropdown.Option(x) for x in ["Integral", "Inicial", "Primaria", "Media General"]],
        value=plan_data.get("nivel_educativo") or "Integral",
        content_padding=ft.Padding(12, 14), **_DROPDOWN,
    )
    necesidad_campo = ft.TextField(
        hint_text="Necesidad detectada",
        value=plan_data.get("necesidad_detectada", ""),
        multiline=True, min_lines=2, max_lines=3,
        content_padding=ft.Padding(14, 14), **_CAMPO,
    )
    resultado_esperado_campo = ft.TextField(
        hint_text="¿Qué espera lograr al finalizar?",
        value=plan_data.get("resultado_esperado", ""),
        multiline=True, min_lines=2, max_lines=3,
        content_padding=ft.Padding(14, 14), **_CAMPO,
    )

    # ── Resultado Obtenido: solo en edición de actividad Completada ──
    estado_actual = actividad.get("estado", "Planificada") if editando else "Planificada"
    mostrar_resultado_obtenido = editando and estado_actual == "Completada"
    resultado_obtenido_campo = ft.TextField(
        hint_text="Resumen del resultado obtenido",
        value=plan_data.get("resultado_obtenido", ""),
        multiline=True, min_lines=2, max_lines=3,
        content_padding=ft.Padding(14, 14), **_CAMPO,
    )

    # ── DatePicker ──
    _MESES = {1:"Ene",2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",
              7:"Jul",8:"Ago",9:"Sep",10:"Oct",11:"Nov",12:"Dic"}

    def _format_fecha(d):
        if d:
            return f"{d.day:02d}/{_MESES.get(d.month,'')}/{d.year}"
        return "Seleccionar…"

    _fecha_ini_default = None
    _fecha_fin_default = None
    if editando:
        fi = actividad.get("fecha_inicio")
        ff = actividad.get("fecha_fin")
        _fecha_ini_default = fi if isinstance(fi, date) else date.today()
        _fecha_fin_default = ff if isinstance(ff, date) else date.today()
    else:
        _fecha_ini_default = date.today()
        _fecha_fin_default = date.today()

    _fecha_ini_sel = {"valor": _fecha_ini_default}
    _fecha_fin_sel = {"valor": _fecha_fin_default}

    texto_fecha_ini = ft.Text(
        _format_fecha(_fecha_ini_default), size=14,
        color=COLOR_TEXTO if _fecha_ini_default else COLOR_TEXTO_SEC, expand=True,
    )
    texto_fecha_fin = ft.Text(
        _format_fecha(_fecha_fin_default), size=14,
        color=COLOR_TEXTO if _fecha_fin_default else COLOR_TEXTO_SEC, expand=True,
    )

    def _on_fecha_ini_change(e):
        picked = e.control.value
        if picked:
            if isinstance(picked, datetime):
                picked = picked.date()
            _fecha_ini_sel["valor"] = picked
            texto_fecha_ini.value = _format_fecha(picked)
            texto_fecha_ini.color = COLOR_TEXTO
            page.update()

    def _on_fecha_fin_change(e):
        picked = e.control.value
        if picked:
            if isinstance(picked, datetime):
                picked = picked.date()
            _fecha_fin_sel["valor"] = picked
            texto_fecha_fin.value = _format_fecha(picked)
            texto_fecha_fin.color = COLOR_TEXTO
            page.update()

    date_picker_ini = ft.DatePicker(
        first_date=date(2024, 1, 1), last_date=date(2030, 12, 31),
        value=_fecha_ini_default, on_change=_on_fecha_ini_change,
    )
    date_picker_fin = ft.DatePicker(
        first_date=date(2024, 1, 1), last_date=date(2030, 12, 31),
        value=_fecha_fin_default, on_change=_on_fecha_fin_change,
    )
    page.overlay.append(date_picker_ini)
    page.overlay.append(date_picker_fin)

    def _abrir_fecha_ini(_):
        date_picker_ini.open = True
        page.update()

    def _abrir_fecha_fin(_):
        date_picker_fin.open = True
        page.update()

    def _limpiar_overlay():
        for p in (date_picker_ini, date_picker_fin):
            if p in page.overlay:
                page.overlay.remove(p)

    boton_fecha_ini = ft.Container(
        content=ft.Row([ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=COLOR_PRIMARIO), ft.Container(width=4), texto_fecha_ini], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=12, border=ft.Border.all(1, COLOR_BORDE), border_radius=RADIO, bgcolor=COLOR_CARD, on_click=_abrir_fecha_ini, ink=True,
    )
    boton_fecha_fin = ft.Container(
        content=ft.Row([ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=COLOR_PRIMARIO), ft.Container(width=4), texto_fecha_fin], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=12, border=ft.Border.all(1, COLOR_BORDE), border_radius=RADIO, bgcolor=COLOR_CARD, on_click=_abrir_fecha_fin, ink=True,
    )

    # ── Brigada: resolver según rol ──
    brigada_id_fija = None
    dd_brigada = None
    brigada_info_text = None
    brigada_bloqueada = False  # True si directivo sin brigadas

    ctx = resolver_contexto_filtrado(page)

    if editando:
        brigada_id_fija = actividad.get("Brigada_idBrigada")
        nombre_brigada = actividad.get("nombre_brigada", "Brigada")
        brigada_info_text = ft.Container(
            content=ft.Row([ft.Icon(ft.Icons.SHIELD_OUTLINED, size=16, color=COLOR_PRIMARIO), ft.Text(f"{nombre_brigada}", size=14, weight="w600", color=COLOR_PRIMARIO)], spacing=8),
            padding=14, bgcolor=ft.Colors.with_opacity(0.08, COLOR_PRIMARIO), border_radius=RADIO, border=ft.Border.all(1, COLOR_PRIMARIO),
        )
    elif ctx["modo"] in ["sin_acceso", "sin_brigada"]:
        brigada_info_text = ft.Text("No tienes brigadas asignadas o sin acceso.", color="#ef4444", italic=True)
        brigada_bloqueada = True
    elif ctx["modo"] == "brigada" and es_profesor(rol):
        # Profesor: chip readonly con ctx["brigada_rol_id"]
        brigada_id_fija = ctx.get("brigada_rol_id")
        if brigada_id_fija:
            try:
                brigadas = crud_brigada.listar_brigadas(brigada_rol_id=brigada_id_fija)
                nombre_b = brigadas[0]["nombre_brigada"] if brigadas else f"Brigada #{brigada_id_fija}"
            except Exception:
                nombre_b = f"Brigada #{brigada_id_fija}"
            brigada_info_text = ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.SHIELD_OUTLINED, size=16, color=COLOR_PRIMARIO), ft.Text(f"{nombre_b} (automática)", size=14, weight="w600", color=COLOR_PRIMARIO)], spacing=8),
                padding=14, bgcolor=ft.Colors.with_opacity(0.08, COLOR_PRIMARIO), border_radius=RADIO, border=ft.Border.all(1, COLOR_PRIMARIO),
            )
        else:
            brigada_info_text = ft.Text("No tienes brigadas asignadas.", color="#ef4444", italic=True)
            brigada_bloqueada = True
    else:
        # Directivo: dropdown filtrado por institución
        try:
            brigadas_disponibles = crud_brigada.listar_brigadas(institucion_id=ctx.get("institucion_id"))
            if brigadas_disponibles:
                opciones = [ft.dropdown.Option(str(b["idBrigada"]), b["nombre_brigada"]) for b in brigadas_disponibles]
                dd_brigada = ft.Dropdown(hint_text="Seleccione brigada", options=opciones, value=opciones[0].key, content_padding=ft.Padding(12, 14), **_DROPDOWN)
            else:
                brigada_info_text = ft.Text("No hay brigadas institucionales disponibles para planificar actividades.", color="#ef4444", italic=True, size=13)
                brigada_bloqueada = True
        except Exception as e:
            brigada_info_text = ft.Text(str(e), size=13, color="#ef4444", italic=True)
            brigada_bloqueada = True

    # ── Estado ──
    dd_estado = ft.Dropdown(
        options=[ft.dropdown.Option("Planificada"), ft.dropdown.Option("En Progreso"), ft.dropdown.Option("Completada")],
        value=estado_actual, content_padding=ft.Padding(12, 14), **_DROPDOWN,
    )

    def _get_brigada_id():
        if brigada_id_fija: return brigada_id_fija
        if dd_brigada and dd_brigada.value: return int(dd_brigada.value)
        return None

    # ── Toggle sección avanzada ──
    _avanzado_state = {"abierto": editando}  # Expandido por defecto al editar

    campos_avanzados = ft.Column([
        ft.Row([ft.Container(_campo_con_titulo("Momento Escolar", momento_escolar_campo), expand=True), ft.Container(width=12), ft.Container(_campo_con_titulo("Origen", origen_campo), expand=True)], spacing=0),
        ft.Row([ft.Container(_campo_con_titulo("Efeméride (opcional)", efemeride_campo), expand=True), ft.Container(width=12), ft.Container(_campo_con_titulo("Nivel Educativo", nivel_educativo_campo), expand=True)], spacing=0),
        _campo_con_titulo("Necesidad Detectada", necesidad_campo),
        _campo_con_titulo("Resultado Esperado", resultado_esperado_campo),
    ], spacing=0, visible=_avanzado_state["abierto"])

    icono_toggle = ft.Icon(
        ft.Icons.EXPAND_LESS if _avanzado_state["abierto"] else ft.Icons.EXPAND_MORE,
        size=20, color=COLOR_PRIMARIO,
    )
    texto_toggle = ft.Text(
        "Detalles de planificación institucional",
        size=13, weight="w600", color=COLOR_PRIMARIO,
    )
    badge_campos = ft.Text("6 campos opcionales", size=11, color=COLOR_TEXTO_SEC, italic=True)

    def _toggle_avanzado(_):
        _avanzado_state["abierto"] = not _avanzado_state["abierto"]
        campos_avanzados.visible = _avanzado_state["abierto"]
        icono_toggle.icon = ft.Icons.EXPAND_LESS if _avanzado_state["abierto"] else ft.Icons.EXPAND_MORE
        page.update()

    toggle_bar = ft.Container(
        content=ft.Row([icono_toggle, texto_toggle, ft.Container(expand=True), badge_campos], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding(12, 10, 12, 10),
        border_radius=RADIO,
        border=ft.Border.all(1, COLOR_BORDE),
        bgcolor=ft.Colors.with_opacity(0.03, COLOR_PRIMARIO),
        on_click=_toggle_avanzado,
        ink=True,
    )

    # ── Guardar ──
    def on_guardar(_):
        # Validación: título
        if not titulo_campo.value or not titulo_campo.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("El título es obligatorio."), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        # Validación: objetivo
        if not objetivo_campo.value or not objetivo_campo.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("Debe indicar el objetivo o plan de acción de la actividad."), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        # Validación: fechas
        fi, ff = _fecha_ini_sel["valor"], _fecha_fin_sel["valor"]
        if not fi or not ff:
            page.snack_bar = ft.SnackBar(ft.Text("Fechas incompletas."), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        if ff < fi:
            page.snack_bar = ft.SnackBar(ft.Text("La fecha de fin no puede ser anterior a la fecha de inicio."), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        # Validación: brigada
        id_brigada = _get_brigada_id()
        if not id_brigada:
            page.snack_bar = ft.SnackBar(ft.Text("No hay brigada asignada."), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return

        # Serializar JSON — preservar resultado_obtenido si campo no visible
        nuevo_plan = {
            "momento_escolar": momento_escolar_campo.value or "Ordinario",
            "origen_actividad": origen_campo.value or "Cronograma",
            "efemeride": (efemeride_campo.value or "").strip(),
            "necesidad_detectada": (necesidad_campo.value or "").strip(),
            "objetivo_plan": objetivo_campo.value.strip(),
            "nivel_educativo": nivel_educativo_campo.value or "Integral",
            "resultado_esperado": (resultado_esperado_campo.value or "").strip(),
            "resultado_obtenido": (
                resultado_obtenido_campo.value.strip()
                if mostrar_resultado_obtenido
                else plan_data.get("resultado_obtenido", "")
            ),
        }
        json_desc = util_json_plan.serializar_plan(nuevo_plan)

        try:
            if editando:
                success = crud_act.actualizar_actividad(
                    id_actividad=actividad["idActividad"],
                    titulo=titulo_campo.value.strip(),
                    descripcion=json_desc,
                    fecha_inicio=str(fi), fecha_fin=str(ff),
                    estado=dd_estado.value,
                    usuario_id=user_id,
                    es_admin_usuario=es_admin(rol),
                )
            else:
                res = crud_act.crear_actividad(
                    titulo_campo.value.strip(),
                    json_desc,
                    str(fi), str(ff),
                    dd_estado.value,
                    id_brigada,
                    usuario_creador_id=user_id,
                )
                success = bool(res)
        except Exception as e:
            success = False
            print(e)

        if success:
            _limpiar_overlay()
            _cerrar_dialogo(page)
            page.snack_bar = ft.SnackBar(ft.Text("Planificación guardada con éxito"), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success: on_success()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error al persistir."), bgcolor="#ef4444")
            page.snack_bar.open = True
        page.update()

    # ── Construir campos del modal ──
    campos = [
        _campo_con_titulo("Título de la Actividad *", titulo_campo),
        ft.Row([ft.Container(_campo_con_titulo("Fecha Inicio *", boton_fecha_ini), expand=True), ft.Container(width=12), ft.Container(_campo_con_titulo("Fecha Fin *", boton_fecha_fin), expand=True)], spacing=0),
        _campo_con_titulo("Objetivo / Plan de Acción *", objetivo_campo),
    ]

    # Brigada
    if brigada_info_text:
        campos.append(_campo_con_titulo("Brigada Asignada", brigada_info_text))
    elif dd_brigada:
        campos.append(_campo_con_titulo("Brigada Responsable *", dd_brigada))

    # Estado
    campos.append(_campo_con_titulo("Estado de la Actividad", dd_estado))

    # Resultado Obtenido (solo edición de Completada)
    if mostrar_resultado_obtenido:
        campos.append(_campo_con_titulo("Resultado Obtenido", resultado_obtenido_campo))

    # Separador + toggle avanzado
    campos.append(ft.Container(height=4))
    campos.append(toggle_bar)
    campos.append(ft.Container(height=8))
    campos.append(campos_avanzados)

    def _on_cancelar(e):
        _limpiar_overlay()
        _cerrar_dialogo(e.page)

    dialogo = ft.AlertDialog(
        modal=True, bgcolor=COLOR_CARD,
        title=ft.Text("Planificar Actividad" if not editando else "Editar Planificación", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column(campos, scroll=ft.ScrollMode.AUTO, tight=True),
            width=580, height=480, bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(content=ft.Text("Cancelar", color=COLOR_TEXTO), style=ft.ButtonStyle(color=COLOR_TEXTO), on_click=_on_cancelar),
            ft.FilledButton("Guardar Plan", style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, color="white"), on_click=on_guardar),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    _abrir_dialogo(page, dialogo)


# ─── Modal: Confirmar eliminación ─────────────────────────────────────

def _abrir_modal_eliminar(page: ft.Page, actividad: dict, on_success=None, usuario_actual=None):
    """Diálogo de confirmación para eliminar una actividad."""
    usuario_actual = usuario_actual or {}
    rol = usuario_actual.get("rol", "")
    user_id = usuario_actual.get("id")
    titulo = actividad.get("titulo", "esta actividad")

    def on_confirmar(_):
        err = crud_act.eliminar_actividad(
            id_actividad=actividad["idActividad"],
            usuario_id=user_id,
            es_admin_usuario=es_admin(rol),
        )
        _cerrar_dialogo(page)
        if err:
            page.snack_bar = ft.SnackBar(ft.Text(err), bgcolor="#ef4444")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Actividad eliminada."), bgcolor="#22c55e")
            if on_success:
                on_success()
        page.snack_bar.open = True
        page.update()

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Eliminar Actividad", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Esta acción no se puede deshacer. Se eliminará la actividad y sus datos asociados.",
                        size=13, color=COLOR_TEXTO_SEC,
                    ),
                    ft.Container(height=12),
                    ft.Text(f'¿Eliminar «{titulo}»?', size=14, weight="w600", color=COLOR_TEXTO),
                ],
                spacing=0,
            ),
            width=420,
            bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(
                content=ft.Text("Cancelar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500),
                style=ft.ButtonStyle(color=COLOR_TEXTO),
                on_click=lambda e: _cerrar_dialogo(e.page),
            ),
            ft.FilledButton(
                "Eliminar",
                style=ft.ButtonStyle(bgcolor="#ef4444", color="white"),
                on_click=on_confirmar,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    _abrir_dialogo(page, dialogo)


# ─── Tarjeta de actividad ────────────────────────────────────────────

def card_actividad(act, usuario_actual, on_complete=None, on_edit=None, on_delete=None, solo_lectura=False):
    """Tarjeta detallada de actividad planificada con chips y resultados de JSON."""
    import util_json_plan
    
    titulo = act.get("titulo", "Sin título")
    desc_raw = act.get("descripcion", "")
    fecha_inicio = str(act.get("fecha_inicio", ""))
    fecha_fin = str(act.get("fecha_fin", ""))
    estado = act.get("estado", "Pendiente")
    brigada = act.get("nombre_brigada", "General")
    creador_id = act.get("creador_id")

    # Deserializar la estructura del plan
    plan = util_json_plan.deserializar_plan(desc_raw)
    objetivo = plan.get("objetivo_plan", "")
    resultado_obtenido = plan.get("resultado_obtenido", "")
    momento_escolar = plan.get("momento_escolar", "Ordinario")
    origen = plan.get("origen_actividad", "Cronograma")
    nivel = plan.get("nivel_educativo", "Integral")

    rol = usuario_actual.get("rol", "") if usuario_actual else ""
    usuario_id = usuario_actual.get("id") if usuario_actual else None

    es_propietario = usuario_id is not None and (es_admin(rol) or creador_id == usuario_id)
    puede_actuar = es_propietario and not solo_lectura

    puede_completar = puede_actuar and estado != "Completada"
    puede_editar = puede_actuar
    puede_eliminar = puede_actuar

    color_estado = {
        "Completada": ft.Colors.GREEN,
        "Pendiente": ft.Colors.ORANGE,
        "En Progreso": ft.Colors.BLUE,
        "Cancelada": ft.Colors.RED,
    }.get(estado, ft.Colors.GREY)

    acciones = []
    if puede_completar:
        acciones.append(
            ft.IconButton(
                icon=ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED, icon_color="#22c55e", icon_size=20,
                tooltip="Marcar como completada", style=ft.ButtonStyle(padding=4), width=34, height=34,
                on_click=lambda e, aid=act["idActividad"]: on_complete(aid) if on_complete else None,
            )
        )
    if puede_editar:
        acciones.append(
            ft.IconButton(
                icon=ft.Icons.EDIT_OUTLINED, icon_color=COLOR_PRIMARIO, icon_size=20,
                tooltip="Editar plan", style=ft.ButtonStyle(padding=4), width=34, height=34,
                on_click=lambda e, a=act: on_edit(a) if on_edit else None,
            )
        )
    if puede_eliminar:
        acciones.append(
            ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE_ROUNDED, icon_color="#ef4444", icon_size=20,
                tooltip="Eliminar plan", style=ft.ButtonStyle(padding=4), width=34, height=34,
                on_click=lambda e, a=act: on_delete(a) if on_delete else None,
            )
        )

    badge_ajeno = []
    if solo_lectura and not es_admin(rol):
        badge_ajeno.append(
            ft.Container(
                content=ft.Text("Solo lectura", size=9, color=COLOR_TEXTO_SEC, italic=True),
                padding=ft.Padding(6, 2, 6, 2), border_radius=8, border=ft.Border.all(1, COLOR_BORDE),
            )
        )

    # CHIPS INSTITUCIONALES
    chips = ft.Row([
        ft.Container(
            content=ft.Text(f"{momento_escolar}", size=10, weight="bold", color=COLOR_PRIMARIO),
            padding=ft.Padding(8, 4, 8, 4), border_radius=12, bgcolor=ft.Colors.with_opacity(0.1, COLOR_PRIMARIO)
        ),
        ft.Container(
            content=ft.Text(f"{origen}", size=10, weight="bold", color="#6366f1"),
            padding=ft.Padding(8, 4, 8, 4), border_radius=12, bgcolor=ft.Colors.with_opacity(0.1, "#6366f1")
        ),
        ft.Container(
            content=ft.Text(f"Nivel: {nivel}", size=10, weight="bold", color="#f59e0b"),
            padding=ft.Padding(8, 4, 8, 4), border_radius=12, bgcolor=ft.Colors.with_opacity(0.1, "#f59e0b")
        )
    ], spacing=6, wrap=True)

    block_resultado = None
    if estado == "Completada" and resultado_obtenido:
        block_resultado = ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.FLAG_CIRCLE, size=14, color="#22c55e"), ft.Text("Resultado Obtenido", size=11, weight="bold", color="#22c55e")], spacing=4),
                ft.Text(resultado_obtenido, size=13, color=COLOR_TEXTO, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
            ], spacing=2),
            padding=ft.Padding(12, 10, 12, 10), bgcolor=ft.Colors.with_opacity(0.05, "#22c55e"),
            border_radius=8, border=ft.Border(left=ft.BorderSide(3, "#22c55e")), margin=ft.margin.only(top=8)
        )
        # Mostrar el objetivo truncado
        texto_central = ft.Text(objetivo, size=13, color=COLOR_TEXTO_SEC, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS)
    else:
        texto_central = ft.Text(objetivo, size=13, color=COLOR_TEXTO_SEC, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS)

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(titulo, size=16, weight="bold", color=COLOR_TEXTO, expand=True),
                        *acciones,
                        *badge_ajeno,
                        ft.Container(
                            content=ft.Text(estado, size=10, weight="bold", color="white"),
                            padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                            border_radius=12, bgcolor=color_estado,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                chips,
                ft.Container(height=4),
                texto_central,
                block_resultado if block_resultado else ft.Container(height=0),
                ft.Container(height=8),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SHIELD_OUTLINED, size=14, color=COLOR_PRIMARIO),
                        ft.Text(brigada, size=12, color=COLOR_PRIMARIO, weight="w600"),
                        ft.Container(width=10),
                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=14, color=COLOR_TEXTO_SEC),
                        ft.Text(f"{fecha_inicio}  →  {fecha_fin}", size=12, color=COLOR_TEXTO_SEC),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=0,
        ),
        padding=16, bgcolor=COLOR_CARD, border_radius=RADIO,
        border=ft.Border.all(1, COLOR_BORDE), shadow=get_sombra_suave(),
        margin=ft.margin.only(bottom=10),
    )


# ─── Pantalla principal ──────────────────────────────────────────────

def build(page: ft.Page, content_area=None, **kwargs) -> ft.Control:
    usuario = _obtener_usuario_actual(page)
    rol = usuario.get("rol", "")
    user_id = usuario.get("id")
    es_prof = es_profesor(rol)
    brigada_rol_id = usuario.get("Brigada_idBrigada") if not es_admin(rol) else None
    from components import resolver_contexto_filtrado
    ctx_pantalla = resolver_contexto_filtrado(page)
    puede_operar = ctx_pantalla["modo"] in ("institucional", "brigada")
    mensaje_bloqueo = (
        "No posee una brigada asignada. Solicite asignacion a la direccion institucional."
        if ctx_pantalla["modo"] == "sin_brigada"
        else "Sin acceso a actividades."
    )

    def _bloquear_operacion():
        page.snack_bar = ft.SnackBar(ft.Text(mensaje_bloqueo), bgcolor="#ef4444")
        page.snack_bar.open = True
        page.update()

    def refresh():
        if content_area:
            content_area.content = build(page, content_area)
            page.update()

    # ─── Callbacks de acciones ────────────────────────────────────
    def on_completar(id_actividad: int):
        if not puede_operar:
            _bloquear_operacion()
            return
        exito = crud_act.marcar_actividad_completada(
            id_actividad=id_actividad,
            usuario_id=user_id,
            es_admin_usuario=es_admin(rol),
        )
        if exito:
            page.snack_bar = ft.SnackBar(ft.Text("Actividad marcada como completada."), bgcolor="#22c55e")
            page.snack_bar.open = True
            refresh()
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("No se pudo cambiar el estado. Verifique permisos."),
                bgcolor="#ef4444",
            )
            page.snack_bar.open = True
            page.update()

    def on_editar(act: dict):
        if not puede_operar:
            _bloquear_operacion()
            return
        _abrir_modal_actividad(page, on_success=refresh, usuario_actual=usuario, actividad=act)

    def on_eliminar(act: dict):
        if not puede_operar:
            _bloquear_operacion()
            return
        _abrir_modal_eliminar(page, actividad=act, on_success=refresh, usuario_actual=usuario)

    def on_nueva_click(_):
        if not puede_operar:
            _bloquear_operacion()
            return
        _abrir_modal_actividad(page, on_success=refresh, usuario_actual=usuario)

    # ─── Construir lista de actividades ───────────────────────────
    def _construir_lista():
        lista_items = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO)

        try:
            from components import resolver_contexto_filtrado
            ctx = resolver_contexto_filtrado(page)
            if ctx["modo"] in ["sin_acceso", "sin_brigada"]:
                actividades = []
            else:
                actividades = crud_act.obtener_actividades_recientes(
                    50, tipo_brigada=ctx.get("tipo_brigada"), solo_usuario_id=None, brigada_rol_id=ctx.get("brigada_rol_id"), institucion_id=ctx.get("institucion_id")
                )
        except Exception as e:
            print(f"Error cargando actividades: {e}")
            actividades = []

        if actividades:
            for act in actividades:
                es_ajena = (user_id is not None and act.get("creador_id") != user_id and not es_admin(rol))
                lista_items.controls.append(
                    card_actividad(
                        act, usuario,
                        on_complete=on_completar,
                        on_edit=on_editar,
                        on_delete=on_eliminar,
                        solo_lectura=es_ajena, # Aunque esté en mi brigada, indico visualmente si es de otro profesor o subjefe
                    )
                )
        else:
            lista_items.controls.append(
                ft.Text("No hay actividades registradas en su brigada.", color=COLOR_TEXTO_SEC, italic=True)
            )
        return lista_items

    lista_ref = ft.Ref[ft.Column]()

    header_items = [
        titulo_pagina(
            "Actividades",
            "Gestión y seguimiento de actividades de las brigadas",
            accion=boton_primario("Nueva Actividad", ft.Icons.ADD, on_click=on_nueva_click) if puede_operar else None,
        ),
    ]

    header_items.append(ft.Container(height=16))
    header_items.append(_construir_lista())

    contenido = ft.Column(
        header_items,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )

    return ft.Container(
        content=contenido,
        padding=24,
        bgcolor=COLOR_FONDO_VERDE,
        expand=True,
    )
