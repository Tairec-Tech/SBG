"""
Estadísticas — Gráficos con flet_charts (BarChart, LineChart, PieChart).
Configuración dinámica por tipo de brigada para coherencia semántica.
Incluye gráficos de planificación: por momento escolar, origen y nivel educativo.
Fallback "En construcción" si flet_charts no está instalado.
"""

import flet as ft
from theme import (
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_FONDO_VERDE,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
    COLOR_PRIMARIO_OSCURO,
    COLOR_VERDE_SUAVE,
    COLOR_BORDE,
)
from components import titulo_pagina, card_principal, card_kpi
import database.crud_estadisticas as crud_est

# Gráficos: paquete opcional (pip install flet-charts)
try:
    import flet_charts as fch
    HAS_CHARTS = True
except ImportError:
    fch = None
    HAS_CHARTS = False

# ==============================================================
# CONFIGURACIÓN SEMÁNTICA POR TIPO DE BRIGADA (11 brigadas)
# ==============================================================

_CONFIG_BRIGADA = {
    "ecologica": {
        "titulo": "Centro de Mando — Brigada Ecológica",
        "subtitulo": "Monitoreo del avance e impacto ambiental",
        "kpi_voluntarios": ("Voluntarios", ft.Icons.PEOPLE_ALT_ROUNDED, ft.Colors.BLUE),
        "kpi_horas": ("Horas Ecológicas", ft.Icons.ECO_ROUNDED, ft.Colors.GREEN),
        "kpi_despliegue": ("Despliegue", ft.Icons.SHARE_LOCATION_ROUNDED, ft.Colors.ORANGE),
        "kpi_impactos": ("Impactos Ambientales", ft.Icons.PUBLIC_ROUNDED, ft.Colors.PURPLE),
        "kpi_efectividad": ("Efectividad", ft.Icons.TRENDING_UP_ROUNDED, ft.Colors.TEAL),
        "chart_barras_titulo": "📊 Jornadas Ecológicas por Mes",
        "chart_barras_tooltip": "jornadas",
        "chart_linea_titulo": "📈 Tendencia de Reportes Ambientales",
        "chart_pie_titulo": "🍩 Estados de Jornadas Ecológicas",
        "colores_barras": ["#10b981", "#059669", "#047857", "#065f46", "#064e3b", "#022c22"],
        "color_linea": "#10b981",
    },
    "convivencia": {
        "titulo": "Centro de Mando — Convivencia y Paz",
        "subtitulo": "Seguimiento de mediaciones y convivencia escolar",
        "kpi_voluntarios": ("Mediadores", ft.Icons.PEOPLE_ALT_ROUNDED, ft.Colors.BLUE),
        "kpi_horas": ("Horas de Mediación", ft.Icons.HANDSHAKE_ROUNDED, ft.Colors.INDIGO),
        "kpi_despliegue": ("Cobertura", ft.Icons.SHARE_LOCATION_ROUNDED, ft.Colors.ORANGE),
        "kpi_impactos": ("Casos Documentados", ft.Icons.DESCRIPTION_ROUNDED, ft.Colors.PURPLE),
        "kpi_efectividad": ("Resolución", ft.Icons.TRENDING_UP_ROUNDED, ft.Colors.TEAL),
        "chart_barras_titulo": "📊 Actividades de Mediación por Mes",
        "chart_barras_tooltip": "mediaciones",
        "chart_linea_titulo": "📈 Tendencia de Reportes de Convivencia",
        "chart_pie_titulo": "🍩 Estados de Actividades de Convivencia",
        "colores_barras": ["#6366f1", "#4f46e5", "#4338ca", "#3730a3", "#312e81", "#1e1b4b"],
        "color_linea": "#6366f1",
    },
    "riesgo": {
        "titulo": "Centro de Mando — Gestión de Riesgo",
        "subtitulo": "Control operativo de prevención y respuesta ante riesgos",
        "kpi_voluntarios": ("Operadores", ft.Icons.PEOPLE_ALT_ROUNDED, ft.Colors.BLUE),
        "kpi_horas": ("Horas de Prevención", ft.Icons.HEALTH_AND_SAFETY_ROUNDED, ft.Colors.AMBER),
        "kpi_despliegue": ("Despliegue", ft.Icons.SHARE_LOCATION_ROUNDED, ft.Colors.ORANGE),
        "kpi_impactos": ("Riesgos Evaluados", ft.Icons.WARNING_AMBER_ROUNDED, ft.Colors.RED),
        "kpi_efectividad": ("Efectividad", ft.Icons.TRENDING_UP_ROUNDED, ft.Colors.TEAL),
        "chart_barras_titulo": "📊 Simulacros y Operativos por Mes",
        "chart_barras_tooltip": "operativos",
        "chart_linea_titulo": "📈 Tendencia de Reportes de Riesgo",
        "chart_pie_titulo": "🍩 Estados de Operativos",
        "colores_barras": ["#f59e0b", "#d97706", "#b45309", "#92400e", "#78350f", "#451a03"],
        "color_linea": "#f59e0b",
    },
    "patrulla": {
        "titulo": "Centro de Mando — Patrulla Escolar",
        "subtitulo": "Supervisión de seguridad vial y vigilancia escolar",
        "kpi_voluntarios": ("Patrulleros", ft.Icons.PEOPLE_ALT_ROUNDED, ft.Colors.BLUE),
        "kpi_horas": ("Horas de Vigilancia", ft.Icons.SHIELD_ROUNDED, ft.Colors.CYAN),
        "kpi_despliegue": ("Cobertura", ft.Icons.SHARE_LOCATION_ROUNDED, ft.Colors.ORANGE),
        "kpi_impactos": ("Incidencias Reportadas", ft.Icons.REPORT_ROUNDED, ft.Colors.RED),
        "kpi_efectividad": ("Efectividad", ft.Icons.TRENDING_UP_ROUNDED, ft.Colors.TEAL),
        "chart_barras_titulo": "📊 Turnos de Vigilancia por Mes",
        "chart_barras_tooltip": "turnos",
        "chart_linea_titulo": "📈 Tendencia de Reportes de Patrulla",
        "chart_pie_titulo": "🍩 Estados de Operaciones de Patrulla",
        "colores_barras": ["#06b6d4", "#0891b2", "#0e7490", "#155e75", "#164e63", "#083344"],
        "color_linea": "#06b6d4",
    },
    "auxilios": {
        "titulo": "Centro de Mando — Primeros Auxilios",
        "subtitulo": "Atención inmediata y prevención de salud escolar",
        "kpi_voluntarios": ("Auxiliadores", ft.Icons.PEOPLE_ALT_ROUNDED, ft.Colors.BLUE),
        "kpi_horas": ("Horas de Atención", ft.Icons.MEDICAL_SERVICES_ROUNDED, ft.Colors.AMBER),
        "kpi_despliegue": ("Cobertura", ft.Icons.SHARE_LOCATION_ROUNDED, ft.Colors.ORANGE),
        "kpi_impactos": ("Casos Atendidos", ft.Icons.HEALING_ROUNDED, ft.Colors.RED),
        "kpi_efectividad": ("Efectividad", ft.Icons.TRENDING_UP_ROUNDED, ft.Colors.TEAL),
        "chart_barras_titulo": "📊 Atenciones por Mes",
        "chart_barras_tooltip": "atenciones",
        "chart_linea_titulo": "📈 Tendencia de Reportes de Auxilios",
        "chart_pie_titulo": "🍩 Estados de Actividades de Auxilios",
        "colores_barras": ["#eab308", "#ca8a04", "#a16207", "#854d0e", "#713f12", "#422006"],
        "color_linea": "#eab308",
    },
    "educacion_fisica": {
        "titulo": "Centro de Mando — Educación Física",
        "subtitulo": "Promoción de actividad física y recreación",
        "kpi_voluntarios": ("Promotores", ft.Icons.PEOPLE_ALT_ROUNDED, ft.Colors.BLUE),
        "kpi_horas": ("Horas Deportivas", ft.Icons.SPORTS_ROUNDED, ft.Colors.BLUE),
        "kpi_despliegue": ("Cobertura", ft.Icons.SHARE_LOCATION_ROUNDED, ft.Colors.ORANGE),
        "kpi_impactos": ("Jornadas Realizadas", ft.Icons.EMOJI_EVENTS_ROUNDED, ft.Colors.PURPLE),
        "kpi_efectividad": ("Efectividad", ft.Icons.TRENDING_UP_ROUNDED, ft.Colors.TEAL),
        "chart_barras_titulo": "📊 Jornadas Deportivas por Mes",
        "chart_barras_tooltip": "jornadas",
        "chart_linea_titulo": "📈 Tendencia de Reportes Deportivos",
        "chart_pie_titulo": "🍩 Estados de Jornadas Deportivas",
        "colores_barras": ["#3b82f6", "#2563eb", "#1d4ed8", "#1e40af", "#1e3a8a", "#172554"],
        "color_linea": "#3b82f6",
    },
    "conuco": {
        "titulo": "Centro de Mando — Mi Conuco Escolar",
        "subtitulo": "Agricultura escolar, huertos y soberanía alimentaria",
        "kpi_voluntarios": ("Cultivadores", ft.Icons.PEOPLE_ALT_ROUNDED, ft.Colors.BLUE),
        "kpi_horas": ("Horas de Cultivo", ft.Icons.AGRICULTURE_ROUNDED, ft.Colors.GREEN),
        "kpi_despliegue": ("Parcelas Activas", ft.Icons.SHARE_LOCATION_ROUNDED, ft.Colors.ORANGE),
        "kpi_impactos": ("Cosechas Documentadas", ft.Icons.COMPOST_ROUNDED, ft.Colors.PURPLE),
        "kpi_efectividad": ("Efectividad", ft.Icons.TRENDING_UP_ROUNDED, ft.Colors.TEAL),
        "chart_barras_titulo": "📊 Actividades de Conuco por Mes",
        "chart_barras_tooltip": "labores",
        "chart_linea_titulo": "📈 Tendencia de Reportes de Conuco",
        "chart_pie_titulo": "🍩 Estados de Labores de Conuco",
        "colores_barras": ["#84cc16", "#65a30d", "#4d7c0f", "#3f6212", "#365314", "#1a2e05"],
        "color_linea": "#84cc16",
    },
    "patrimonio": {
        "titulo": "Centro de Mando — Patrimonio y Turismo",
        "subtitulo": "Valoración de identidad local y patrimonio histórico-cultural",
        "kpi_voluntarios": ("Promotores", ft.Icons.PEOPLE_ALT_ROUNDED, ft.Colors.BLUE),
        "kpi_horas": ("Horas Culturales", ft.Icons.MUSEUM_ROUNDED, ft.Colors.PINK),
        "kpi_despliegue": ("Cobertura", ft.Icons.SHARE_LOCATION_ROUNDED, ft.Colors.ORANGE),
        "kpi_impactos": ("Actividades Culturales", ft.Icons.CASTLE_ROUNDED, ft.Colors.PURPLE),
        "kpi_efectividad": ("Efectividad", ft.Icons.TRENDING_UP_ROUNDED, ft.Colors.TEAL),
        "chart_barras_titulo": "📊 Actividades Culturales por Mes",
        "chart_barras_tooltip": "actividades",
        "chart_linea_titulo": "📈 Tendencia de Reportes de Patrimonio",
        "chart_pie_titulo": "🍩 Estados de Actividades Patrimoniales",
        "colores_barras": ["#ec4899", "#db2777", "#be185d", "#9d174d", "#831843", "#500724"],
        "color_linea": "#ec4899",
    },
    "artes": {
        "titulo": "Centro de Mando — Artes Visuales",
        "subtitulo": "Expresión creativa, murales y apoyo visual escolar",
        "kpi_voluntarios": ("Artistas", ft.Icons.PEOPLE_ALT_ROUNDED, ft.Colors.BLUE),
        "kpi_horas": ("Horas Creativas", ft.Icons.PALETTE_ROUNDED, ft.Colors.DEEP_PURPLE),
        "kpi_despliegue": ("Cobertura", ft.Icons.SHARE_LOCATION_ROUNDED, ft.Colors.ORANGE),
        "kpi_impactos": ("Obras Documentadas", ft.Icons.BRUSH_ROUNDED, ft.Colors.PURPLE),
        "kpi_efectividad": ("Efectividad", ft.Icons.TRENDING_UP_ROUNDED, ft.Colors.TEAL),
        "chart_barras_titulo": "📊 Proyectos Artísticos por Mes",
        "chart_barras_tooltip": "proyectos",
        "chart_linea_titulo": "📈 Tendencia de Reportes de Artes",
        "chart_pie_titulo": "🍩 Estados de Proyectos Artísticos",
        "colores_barras": ["#a855f7", "#9333ea", "#7e22ce", "#6b21a8", "#581c87", "#3b0764"],
        "color_linea": "#a855f7",
    },
    "patriotica": {
        "titulo": "Centro de Mando — Juventud Patriótica",
        "subtitulo": "Identidad nacional, efemérides y memoria histórica",
        "kpi_voluntarios": ("Jóvenes", ft.Icons.PEOPLE_ALT_ROUNDED, ft.Colors.BLUE),
        "kpi_horas": ("Horas Cívicas", ft.Icons.FLAG_ROUNDED, ft.Colors.BLUE_GREY),
        "kpi_despliegue": ("Cobertura", ft.Icons.SHARE_LOCATION_ROUNDED, ft.Colors.ORANGE),
        "kpi_impactos": ("Actos Documentados", ft.Icons.ACCOUNT_BALANCE_ROUNDED, ft.Colors.PURPLE),
        "kpi_efectividad": ("Efectividad", ft.Icons.TRENDING_UP_ROUNDED, ft.Colors.TEAL),
        "chart_barras_titulo": "📊 Actos Cívicos por Mes",
        "chart_barras_tooltip": "actos",
        "chart_linea_titulo": "📈 Tendencia de Reportes Cívicos",
        "chart_pie_titulo": "🍩 Estados de Actos Cívicos",
        "colores_barras": ["#9ca3af", "#6b7280", "#4b5563", "#374151", "#1f2937", "#111827"],
        "color_linea": "#9ca3af",
    },
    "ddhh": {
        "titulo": "Centro de Mando — Derechos Humanos",
        "subtitulo": "Dignidad, igualdad, inclusión y cultura de derechos",
        "kpi_voluntarios": ("Promotores", ft.Icons.PEOPLE_ALT_ROUNDED, ft.Colors.BLUE),
        "kpi_horas": ("Horas Formativas", ft.Icons.GAVEL_ROUNDED, ft.Colors.INDIGO),
        "kpi_despliegue": ("Cobertura", ft.Icons.SHARE_LOCATION_ROUNDED, ft.Colors.ORANGE),
        "kpi_impactos": ("Casos Documentados", ft.Icons.BALANCE_ROUNDED, ft.Colors.PURPLE),
        "kpi_efectividad": ("Efectividad", ft.Icons.TRENDING_UP_ROUNDED, ft.Colors.TEAL),
        "chart_barras_titulo": "📊 Actividades de DDHH por Mes",
        "chart_barras_tooltip": "actividades",
        "chart_linea_titulo": "📈 Tendencia de Reportes de DDHH",
        "chart_pie_titulo": "🍩 Estados de Actividades de DDHH",
        "colores_barras": ["#1e3a8a", "#1e40af", "#1d4ed8", "#2563eb", "#3b82f6", "#60a5fa"],
        "color_linea": "#1e3a8a",
    },
}

# Configuración por defecto (vista global, sin brigada activa)
_CONFIG_DEFAULT = {
    "titulo": "Centro de Mando Estadístico",
    "subtitulo": "Monitoreo global del avance e impacto de todas las brigadas",
    "kpi_voluntarios": ("Brigadistas", ft.Icons.PEOPLE_ALT_ROUNDED, ft.Colors.BLUE),
    "kpi_horas": ("Horas Registradas", ft.Icons.HOURGLASS_BOTTOM_ROUNDED, ft.Colors.GREEN),
    "kpi_despliegue": ("Despliegue", ft.Icons.SHARE_LOCATION_ROUNDED, ft.Colors.ORANGE),
    "kpi_impactos": ("Impactos", ft.Icons.PUBLIC_ROUNDED, ft.Colors.PURPLE),
    "kpi_efectividad": ("Efectividad", ft.Icons.TRENDING_UP_ROUNDED, ft.Colors.TEAL),
    "chart_barras_titulo": "📊 Actividades por Mes",
    "chart_barras_tooltip": "actividades",
    "chart_linea_titulo": "📈 Tendencia de Reportes",
    "chart_pie_titulo": "🍩 Distribución de Estados de Actividades",
    "colores_barras": ["#10b981", "#059669", "#047857", "#065f46", "#064e3b", "#022c22"],
    "color_linea": "#10b981",
}


def _get_config(tipo_brigada: str | None) -> dict:
    """Devuelve la configuración semántica para el tipo de brigada activo."""
    if tipo_brigada and tipo_brigada in _CONFIG_BRIGADA:
        return _CONFIG_BRIGADA[tipo_brigada]
    return _CONFIG_DEFAULT


def _tarjeta_grafico(titulo: str, grafico: ft.Control, altura: float = 320) -> ft.Container:
    return card_principal(
        ft.Column(
            [
                ft.Text(titulo, size=18, weight="bold", color=COLOR_TEXTO),
                ft.Container(height=20),
                ft.Container(content=grafico, height=altura),
            ],
            spacing=0,
        ),
        padding=24,
    )


def _seccion_titulo(titulo: str, icono=ft.Icons.ANALYTICS_ROUNDED):
    """Encabezado visual para secciones de gráficos."""
    return ft.Container(
        content=ft.Row([
            ft.Icon(icono, size=20, color=COLOR_PRIMARIO),
            ft.Container(width=8),
            ft.Text(titulo, size=16, weight="w600", color=COLOR_TEXTO),
        ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding(0, 24, 0, 12),
    )


def _build_kpis(kpis, cfg):
    lbl_vol, ico_vol, clr_vol = cfg["kpi_voluntarios"]
    lbl_hrs, ico_hrs, clr_hrs = cfg["kpi_horas"]
    lbl_dep, ico_dep, clr_dep = cfg["kpi_despliegue"]
    lbl_imp, ico_imp, clr_imp = cfg["kpi_impactos"]
    lbl_efe, ico_efe, clr_efe = cfg["kpi_efectividad"]

    return ft.Row(
        [
            ft.Container(card_kpi(lbl_vol, kpis.get("voluntariado_activo", 0), ico_vol, clr_vol), expand=True),
            ft.Container(card_kpi(lbl_hrs, kpis.get("horas_invertidas", 0), ico_hrs, clr_hrs), expand=True),
            ft.Container(card_kpi(lbl_dep, f"{kpis.get('despliegue_operativo', 0)}%", ico_dep, clr_dep), expand=True),
            ft.Container(card_kpi(lbl_imp, kpis.get("impacto_documentado", 0), ico_imp, clr_imp), expand=True),
            ft.Container(card_kpi(lbl_efe, f"{kpis.get('tasa_efectividad', 0)}%", ico_efe, clr_efe), expand=True),
        ],
        spacing=16,
        alignment=ft.MainAxisAlignment.START,
    )

def _build_bar_chart(act_por_mes, cfg, tooltip_barras):
    bar_groups = []
    bar_labels = []
    meses_es = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
                7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
    colores_barras = cfg["colores_barras"]

    if not act_por_mes:
        bar_labels.append(fch.ChartAxisLabel(value=0, label=ft.Container(ft.Text("Sin datos", size=11, color=COLOR_TEXTO_SEC), padding=8)))
        bar_groups.append(fch.BarChartGroup(x=0, rods=[fch.BarChartRod(from_y=0, to_y=0, width=36, color=COLOR_BORDE, border_radius=8)]))
    else:
        for index, item in enumerate(act_por_mes):
            mes_str = item[0]
            cantidad = item[1]
            try:
                mes_num = int(mes_str.split("-")[1])
                nombre_mes = meses_es.get(mes_num, mes_str)
            except:
                nombre_mes = mes_str

            bar_labels.append(fch.ChartAxisLabel(
                value=index,
                label=ft.Container(ft.Text(nombre_mes, size=12, weight="w500", color=COLOR_TEXTO_SEC), padding=ft.padding.only(top=8))
            ))
            color_barra = colores_barras[index % len(colores_barras)]
            bar_groups.append(fch.BarChartGroup(
                x=index,
                rods=[fch.BarChartRod(
                    from_y=0, to_y=cantidad, width=36, color=color_barra, border_radius=8,
                    tooltip=f"{nombre_mes}: {cantidad} {tooltip_barras}",
                )],
            ))
    max_actividades = max([item[1] for item in act_por_mes]) if act_por_mes else 10
    return fch.BarChart(
        expand=True, interactive=True, max_y=max_actividades + max(5, int(max_actividades * 0.25)),
        border=ft.Border.all(1, COLOR_BORDE),
        horizontal_grid_lines=fch.ChartGridLines(color=ft.Colors.with_opacity(0.1, "grey"), width=1, dash_pattern=[4, 4]),
        left_axis=fch.ChartAxis(label_size=40, title=ft.Text(tooltip_barras.capitalize(), size=12, color=COLOR_TEXTO_SEC, weight="w500"), title_size=42),
        bottom_axis=fch.ChartAxis(label_size=48, labels=bar_labels),
        groups=bar_groups,
    )

def _build_line_chart(reportes_tendencia, cfg):
    puntos_linea = []
    line_labels = []
    meses_es = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
                7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
    if not reportes_tendencia:
        puntos_linea.append(fch.LineChartDataPoint(0, 0))
        puntos_linea.append(fch.LineChartDataPoint(1, 0))
        line_labels.append(fch.ChartAxisLabel(value=0, label=ft.Text("-", size=11, color=COLOR_TEXTO_SEC)))
    else:
        for idx, rt in enumerate(reportes_tendencia):
            mes_str = rt[0]
            val = rt[1]
            try:
                mes_num = int(mes_str.split("-")[1])
                nombre_mes = meses_es.get(mes_num, mes_str)
            except:
                nombre_mes = mes_str

            puntos_linea.append(fch.LineChartDataPoint(idx, val, tooltip=f"{nombre_mes}: {val} reportes"))
            line_labels.append(fch.ChartAxisLabel(value=idx, label=ft.Container(ft.Text(nombre_mes, size=12, weight="w500", color=COLOR_TEXTO_SEC), padding=ft.padding.only(top=6))))
    max_reportes = max([item[1] for item in reportes_tendencia]) if reportes_tendencia else 10
    return fch.LineChart(
        expand=True,
        data_series=[fch.LineChartData(stroke_width=4, color=cfg["color_linea"], curved=True, rounded_stroke_cap=True, points=puntos_linea)],
        min_y=0, max_y=max_reportes + max(3, int(max_reportes * 0.25)), min_x=0, max_x=max(len(puntos_linea)-1, 1),
        border=ft.Border.all(1, COLOR_BORDE),
        horizontal_grid_lines=fch.ChartGridLines(color=ft.Colors.with_opacity(0.1, "grey"), width=1, dash_pattern=[4, 4]),
        left_axis=fch.ChartAxis(label_size=40, show_labels=True), bottom_axis=fch.ChartAxis(label_size=48, labels=line_labels),
    )

def _build_pie_chart(estados):
    pie_sections = []
    leyenda_items = []
    colores_estados = {
        "Completada": "#10b981",
        "Pendiente": "#3b82f6",
        "Planificada": "#8b5cf6",
        "En progreso": "#f59e0b",
        "En Progreso": "#f59e0b",
        "Cancelada": "#ef4444",
    }
    if not estados:
        pie_sections.append(fch.PieChartSection(value=100, title="Sin Datos", color=COLOR_BORDE, radius=80, title_style=ft.TextStyle(size=13, color=COLOR_TEXTO_SEC, weight="bold")))
    else:
        total_actividades = sum([e["conteo"] for e in estados])
        for est in estados:
            nombre = est.get("estado", "Otro")
            conteo = est["conteo"]
            color_est = colores_estados.get(nombre, "#94a3b8")
            porcentaje = (conteo / total_actividades) * 100 if total_actividades > 0 else 0
            titulo_seccion = f"{int(porcentaje)}%" if porcentaje > 8 else ""
            pie_sections.append(fch.PieChartSection(value=conteo, title=titulo_seccion, color=color_est, radius=80, title_style=ft.TextStyle(size=13, color=ft.Colors.WHITE, weight="bold")))
            leyenda_items.append(ft.Row([
                ft.Container(width=14, height=14, bgcolor=color_est, border_radius=4),
                ft.Container(width=8), ft.Text(f"{nombre}", size=13, color=COLOR_TEXTO, weight="w500"),
                ft.Container(width=4), ft.Text(f"({conteo} — {int(porcentaje)}%)", size=12, color=COLOR_TEXTO_SEC)
            ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    return fch.PieChart(expand=True, sections_space=3, center_space_radius=46, center_space_color=ft.Colors.SURFACE, sections=pie_sections), leyenda_items


# ==============================================================
# GRÁFICOS DE PLANIFICACIÓN (Momento, Origen, Nivel)
# ==============================================================

_COLORES_PLANIFICACION = {
    "momento": ["#8b5cf6", "#7c3aed", "#6d28d9", "#5b21b6", "#4c1d95"],
    "origen": ["#f59e0b", "#3b82f6", "#10b981", "#ef4444", "#6366f1"],
    "nivel": ["#14b8a6", "#f97316", "#8b5cf6", "#ec4899", "#06b6d4"],
}


def _build_bar_chart_categorias(datos, colores_key, tooltip_label, titulo_eje=""):
    """BarChart genérico para datos categorizados [{nombre, conteo}]."""
    if not datos:
        # Empty state limpio
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ANALYTICS_OUTLINED, size=36, color=COLOR_BORDE),
                ft.Container(height=8),
                ft.Text("Sin datos de planificación", size=14, color=COLOR_TEXTO_SEC),
                ft.Text("Los datos aparecerán cuando haya actividades con planificación estructurada.",
                         size=12, color=COLOR_TEXTO_SEC, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
        height=200, alignment=ft.Alignment(0, 0),
        )

    colores = _COLORES_PLANIFICACION.get(colores_key, _COLORES_PLANIFICACION["momento"])
    bar_groups = []
    bar_labels = []

    for i, item in enumerate(datos[:8]):  # Limitar a 8 categorías max
        nombre = item["nombre"]
        conteo = item["conteo"]
        color = colores[i % len(colores)]

        # Truncar nombres largos
        nombre_corto = nombre[:12] + "…" if len(nombre) > 12 else nombre
        bar_labels.append(fch.ChartAxisLabel(
            value=i,
            label=ft.Container(
                ft.Text(nombre_corto, size=10, weight="w500", color=COLOR_TEXTO_SEC),
                padding=ft.padding.only(top=6),
            )
        ))
        bar_groups.append(fch.BarChartGroup(
            x=i,
            rods=[fch.BarChartRod(
                from_y=0, to_y=conteo, width=32, color=color, border_radius=8,
                tooltip=f"{nombre}: {conteo} {tooltip_label}",
            )],
        ))

    max_val = max(item["conteo"] for item in datos) if datos else 5
    return fch.BarChart(
        expand=True, interactive=True,
        max_y=max_val + max(3, int(max_val * 0.3)),
        border=ft.Border.all(1, COLOR_BORDE),
        horizontal_grid_lines=fch.ChartGridLines(color=ft.Colors.with_opacity(0.1, "grey"), width=1, dash_pattern=[4, 4]),
        left_axis=fch.ChartAxis(label_size=40),
        bottom_axis=fch.ChartAxis(label_size=48, labels=bar_labels),
        groups=bar_groups,
    )


def _build_pie_chart_categorias(datos, colores_key, titulo_vacio="Sin datos"):
    """PieChart genérico para datos categorizados [{nombre, conteo}]."""
    colores = _COLORES_PLANIFICACION.get(colores_key, _COLORES_PLANIFICACION["momento"])

    if not datos:
        pie = fch.PieChart(
            sections=[fch.PieChartSection(value=100, title=titulo_vacio, color=COLOR_BORDE, radius=70,
                                          title_style=ft.TextStyle(size=12, color=COLOR_TEXTO_SEC, weight="bold"))],
            expand=True, sections_space=0, center_space_radius=40, center_space_color=ft.Colors.SURFACE,
        )
        return pie, [ft.Text("Sin datos disponibles.", color=COLOR_TEXTO_SEC, italic=True, size=12)]

    total = sum(d["conteo"] for d in datos)
    sections = []
    leyenda = []

    for i, item in enumerate(datos[:6]):
        color = colores[i % len(colores)]
        pct = (item["conteo"] / total * 100) if total > 0 else 0
        label = f"{int(pct)}%" if pct > 8 else ""
        sections.append(fch.PieChartSection(
            value=item["conteo"], title=label, color=color, radius=70,
            title_style=ft.TextStyle(size=12, color=ft.Colors.WHITE, weight="bold"),
        ))
        leyenda.append(ft.Row([
            ft.Container(width=12, height=12, bgcolor=color, border_radius=3),
            ft.Container(width=6),
            ft.Text(item["nombre"], size=12, color=COLOR_TEXTO, weight="w500"),
            ft.Container(width=4),
            ft.Text(f"({item['conteo']})", size=11, color=COLOR_TEXTO_SEC),
        ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER))

    pie = fch.PieChart(
        expand=True, sections_space=2, center_space_radius=40,
        center_space_color=ft.Colors.SURFACE, sections=sections,
    )
    return pie, leyenda


# ==============================================================
# BUILD PRINCIPAL
# ==============================================================

def _build_con_graficos(page: ft.Page) -> ft.Control:
    # 1. Obtener tipo de brigada y cfg sincrónicamente
    from components import resolver_contexto_filtrado
    ctx = resolver_contexto_filtrado(page)
    _tb = ctx.get("tipo_brigada")
    brigada_rol_id = ctx.get("brigada_rol_id")
    _inst_id = ctx.get("institucion_id")
    cfg = _get_config(_tb)

    _ck_prefix = f"_{ctx['modo']}_{ctx.get('institucion_id')}_{ctx.get('brigada_rol_id')}"
    ck_kpis = f"{_ck_prefix}_kpis"
    ck_bar  = f"{_ck_prefix}_bar"
    ck_line = f"{_ck_prefix}_line"
    ck_pie  = f"{_ck_prefix}_pie"
    ck_momento = f"{_ck_prefix}_momento"
    ck_origen  = f"{_ck_prefix}_origen"
    ck_nivel   = f"{_ck_prefix}_nivel"
    
    loading_key = f"{_ck_prefix}_loading"
    loaded_key = f"{_ck_prefix}_loaded"
    
    is_loaded = bool(page.data.get(loaded_key))
    
    # Contenedores para reemplazo de contenido dinámico
    kpis_container = ft.Container(height=110, alignment=ft.Alignment(0, 0))
    bar_container = ft.Container(height=320, alignment=ft.Alignment(0, 0))
    line_container = ft.Container(height=320, alignment=ft.Alignment(0, 0))
    pie_chart_container = ft.Container(height=280, alignment=ft.Alignment(0, 0), expand=True)
    pie_legend_container = ft.Container(alignment=ft.Alignment(0, 0))

    # Nuevos contenedores para gráficos de planificación
    momento_container = ft.Container(height=250, alignment=ft.Alignment(0, 0))
    origen_chart_container = ft.Container(height=220, alignment=ft.Alignment(0, 0), expand=True)
    origen_legend_container = ft.Container(alignment=ft.Alignment(0, 0))
    nivel_container = ft.Container(height=250, alignment=ft.Alignment(0, 0))

    def popular_vistas():
        kpis_data = page.data.get(ck_kpis, {})
        kpis_container.content = _build_kpis(kpis_data, cfg)
        
        acts_data = page.data.get(ck_bar, [])
        bar_container.content = _build_bar_chart(acts_data, cfg, cfg["chart_barras_tooltip"])
        
        rep_data = page.data.get(ck_line, [])
        line_container.content = _build_line_chart(rep_data, cfg)
        
        est_data = page.data.get(ck_pie, [])
        pie_ch, pie_leg = _build_pie_chart(est_data)
        pie_chart_container.content = pie_ch
        pie_legend_container.content = ft.Column(
            pie_leg if pie_leg else [ft.Text("Sin datos", color=COLOR_TEXTO_SEC, italic=True)],
            spacing=12, alignment=ft.MainAxisAlignment.CENTER,
        )

        # Gráficos de planificación
        momento_data = page.data.get(ck_momento, [])
        momento_container.content = _build_bar_chart_categorias(
            momento_data, "momento", "actividades"
        )

        origen_data = page.data.get(ck_origen, [])
        origen_ch, origen_leg = _build_pie_chart_categorias(
            origen_data, "origen"
        )
        origen_chart_container.content = origen_ch
        origen_legend_container.content = ft.Column(
            origen_leg, spacing=10, alignment=ft.MainAxisAlignment.CENTER,
        )

        nivel_data = page.data.get(ck_nivel, [])
        nivel_container.content = _build_bar_chart_categorias(
            nivel_data, "nivel", "actividades"
        )

    if is_loaded:
        popular_vistas()
    else:
        # Skeletons
        kpis_container.content = ft.ProgressRing()
        bar_container.content = ft.ProgressRing()
        line_container.content = ft.ProgressRing()
        pie_chart_container.content = ft.ProgressRing()
        pie_legend_container.content = ft.Text("Cargando...", color=COLOR_TEXTO_SEC)
        momento_container.content = ft.ProgressRing()
        origen_chart_container.content = ft.ProgressRing()
        origen_legend_container.content = ft.Text("Cargando...", color=COLOR_TEXTO_SEC)
        nivel_container.content = ft.ProgressRing()

    async def _load_data_async():
        if getattr(page, "data", None) is None: return
        if page.data.get(loading_key) or page.data.get(loaded_key): return
        page.data[loading_key] = True

        try:
            import asyncio
            if ctx["modo"] in ["sin_acceso", "sin_brigada"]:
                kpis = {"voluntariado_activo": 0, "horas_invertidas": 0, "despliegue_operativo": 0, "impacto_documentado": 0, "tasa_efectividad": 0}
                act_por_mes = []
                reportes_tendencia = []
                estados = []
                por_momento = []
                por_origen = []
                por_nivel = []
            else:
                kpis = await asyncio.to_thread(crud_est.get_kpis_estadisticas, _tb, brigada_rol_id, _inst_id)
                act_por_mes = await asyncio.to_thread(crud_est.get_actividades_por_mes, _tb, brigada_rol_id, _inst_id)
                reportes_tendencia = await asyncio.to_thread(crud_est.get_tendencia_reportes_por_mes, _tb, brigada_rol_id, _inst_id)
                estados = await asyncio.to_thread(crud_est.get_distribucion_estados_actividades, _tb, brigada_rol_id, _inst_id)

                # Nuevos: planificación
                por_momento = await asyncio.to_thread(crud_est.get_actividades_por_momento, _tb, brigada_rol_id, _inst_id)
                por_origen = await asyncio.to_thread(crud_est.get_actividades_por_origen, _tb, brigada_rol_id, _inst_id)
                por_nivel = await asyncio.to_thread(crud_est.get_actividades_por_nivel, _tb, brigada_rol_id, _inst_id)

            page.data[ck_kpis] = kpis
            page.data[ck_bar] = act_por_mes
            page.data[ck_line] = reportes_tendencia
            page.data[ck_pie] = estados
            page.data[ck_momento] = por_momento
            page.data[ck_origen] = por_origen
            page.data[ck_nivel] = por_nivel
            
            # Popular la vista con los datos ya cacheados
            popular_vistas()
            if page.session: page.update()
            
            # Solo si todo fue bien marcamos como loaded (sin excepciones)
            page.data[loaded_key] = True

        except Exception as e:
            print(f"Error en carga asíncrona de estadísticas: {e}")
        finally:
            page.data[loading_key] = False

    if not is_loaded:
        page.run_task(_load_data_async)

    # ── Layout Principal ──────────────────────────────────────

    # Sección 1: Operacional (existente)
    fila_1 = ft.Row([
        ft.Container(content=_tarjeta_grafico(cfg["chart_barras_titulo"], bar_container), expand=True),
        ft.Container(width=20),
        ft.Container(content=_tarjeta_grafico(cfg["chart_linea_titulo"], line_container), expand=True),
    ], spacing=0)

    contenido_pie = ft.Row([
        pie_chart_container, ft.Container(width=24), pie_legend_container
    ], vertical_alignment=ft.CrossAxisAlignment.CENTER)

    tarjeta_pie = card_principal(
        ft.Column([
            ft.Text(cfg["chart_pie_titulo"], size=18, weight="bold", color=COLOR_TEXTO),
            ft.Container(height=16),
            contenido_pie,
        ], spacing=0), padding=24
    )

    # Sección 2: Planificación Institucional (nueva)
    contenido_origen = ft.Row([
        origen_chart_container, ft.Container(width=24), origen_legend_container
    ], vertical_alignment=ft.CrossAxisAlignment.CENTER)

    tarjeta_origen = card_principal(
        ft.Column([
            ft.Text("🎯 Distribución por Origen de Actividad", size=18, weight="bold", color=COLOR_TEXTO),
            ft.Container(height=16),
            contenido_origen,
        ], spacing=0), padding=24
    )

    fila_planificacion = ft.Row([
        ft.Container(
            content=_tarjeta_grafico("📅 Actividades por Momento Escolar", momento_container, altura=250),
            expand=True,
        ),
        ft.Container(width=20),
        ft.Container(
            content=_tarjeta_grafico("🎓 Actividades por Nivel Educativo", nivel_container, altura=250),
            expand=True,
        ),
    ], spacing=0)

    return ft.Column(
        [
            titulo_pagina(cfg["titulo"], cfg["subtitulo"]),
            ft.Container(height=16),
            kpis_container,
            ft.Container(height=24),
            fila_1,
            ft.Container(height=24),
            tarjeta_pie,
            # Sección de planificación con separador visual
            _seccion_titulo("Análisis de Planificación Institucional", ft.Icons.SCHOOL_ROUNDED),
            fila_planificacion,
            ft.Container(height=20),
            tarjeta_origen,
            ft.Container(height=24),
        ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=0
    )


def _build_sin_graficos() -> ft.Control:
    """Vista cuando flet_charts no está instalado."""
    return ft.Column(
        [
            titulo_pagina(
                "Estadísticas",
                "Sistema de coordinación de brigadas escolares",
            ),
            ft.Container(height=32),
            card_principal(
                ft.Column(
                    [
                        ft.Icon(ft.Icons.CONSTRUCTION_OUTLINED, color=COLOR_PRIMARIO, size=64),
                        ft.Container(height=24),
                        ft.Text("En construcción", size=22, weight="bold", color=COLOR_TEXTO),
                        ft.Container(height=8),
                        ft.Text(
                            "Los gráficos requieren el paquete flet-charts. Instálalo con: pip install flet-charts",
                            size=14,
                            color=COLOR_TEXTO_SEC,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Después reinicia la aplicación.",
                            size=13,
                            color=COLOR_TEXTO_SEC,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
                padding=48,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )


def build(page: ft.Page, **kwargs) -> ft.Control:
    if HAS_CHARTS:
        contenido = _build_con_graficos(page)
    else:
        contenido = _build_sin_graficos()

    return ft.Container(
        content=contenido,
        padding=24,
        bgcolor=COLOR_FONDO_VERDE,
        expand=True,
    )
