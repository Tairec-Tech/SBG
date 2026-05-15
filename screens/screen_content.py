"""Contenido Educativo — guías operativas y pedagógicas de las 11 brigadas escolares."""

import flet as ft

from theme import (
    BRIGADAS,
    COLOR_PRIMARIO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_CARD,
    COLOR_BORDE,
    COLOR_FONDO_VERDE,
    get_sombra_card,
    get_sombra_suave,
)
from components import titulo_pagina, card_principal, resolver_contexto_filtrado
from contenido_educativo import CONTENIDO_EDUCATIVO
from brigadas_catalogo import CATALOGO_BRIGADAS_BASE
from database.crud_brigada import obtener_tipo_brigada_por_id


# ─────────────────────────────────────────────────────────────
# MAPEO DE ICONOS POR SLUG  (fuente: theme.BRIGADAS["icono"])
# Se resuelve con fallback seguro.
# ─────────────────────────────────────────────────────────────
_ICONOS_SLUG = {
    "ecologica":        "ECO_OUTLINED",
    "riesgo":           "HEALTH_AND_SAFETY_OUTLINED",
    "patrulla":         "DIRECTIONS_WALK_OUTLINED",
    "convivencia":      "HANDSHAKE_OUTLINED",
    "auxilios":         "MEDICAL_SERVICES_OUTLINED",
    "educacion_fisica": "SPORTS_BASKETBALL_OUTLINED",
    "conuco":           "AGRICULTURE_OUTLINED",
    "patrimonio":       "MUSEUM_OUTLINED",
    "artes":            "PALETTE_OUTLINED",
    "patriotica":       "FLAG_OUTLINED",
    "ddhh":             "GAVEL_OUTLINED",
}

_FALLBACK_ICON = ft.Icons.MENU_BOOK_OUTLINED


def _icono(slug: str):
    """Resuelve un icono Flet por slug con fallback seguro."""
    nombre = _ICONOS_SLUG.get(slug)
    if nombre:
        return getattr(ft.Icons, nombre, _FALLBACK_ICON)
    return _FALLBACK_ICON


def _color_brigada(slug: str):
    """Obtiene el color primario hex de una brigada desde theme.BRIGADAS."""
    info = BRIGADAS.get(slug, {})
    return info.get("hex_primario", "#64748b")


def _color_brigada_oscuro(slug: str):
    """Obtiene el color primario oscuro hex de una brigada desde theme.BRIGADAS."""
    info = BRIGADAS.get(slug, {})
    return info.get("hex_primario_oscuro", "#475569")


def _nombre_brigada(slug: str):
    """Obtiene el nombre oficial de una brigada desde theme.BRIGADAS."""
    info = BRIGADAS.get(slug, {})
    return info.get("nombre", slug.replace("_", " ").title())


# ─────────────────────────────────────────────────────────────
# BUILD PRINCIPAL
# ─────────────────────────────────────────────────────────────
def build(page: ft.Page, **kwargs) -> ft.Control:
    ctx = resolver_contexto_filtrado(page)
    modo = ctx.get("modo")

    # Contenedor dinámico que permite swap entre grid y guía
    contenedor_dinamico = ft.Container(expand=True)

    if modo == "institucional":
        # Directivo/Admin: vista con 11 tarjetas
        contenedor_dinamico.content = _build_grid_tarjetas(page, contenedor_dinamico)

    elif modo == "brigada":
        # Profesor con brigada: guía directa
        usuario = (page.data or {}).get("usuario_actual", {})
        tipo = obtener_tipo_brigada_por_id(usuario.get("Brigada_idBrigada"))
        if tipo and tipo in CONTENIDO_EDUCATIVO:
            contenedor_dinamico.content = _build_vista_guia(page, tipo, mostrar_volver=False)
        else:
            contenedor_dinamico.content = _build_empty_contenido(tipo)

    elif modo == "sin_brigada":
        contenedor_dinamico.content = _build_empty_state_sin_brigada()

    else:
        # sin_acceso u otro caso
        contenedor_dinamico.content = _build_empty_state_sin_acceso(ctx.get("error"))

    contenido = ft.Column(
        [
            titulo_pagina(
                "Contenido Educativo",
                "Guías operativas y pedagógicas de las brigadas escolares",
            ),
            ft.Container(height=24),
            contenedor_dinamico,
        ],
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


# ─────────────────────────────────────────────────────────────
# VISTA INSTITUCIONAL: 11 TARJETAS (DIRECTIVO)
# ─────────────────────────────────────────────────────────────
def _build_grid_tarjetas(page: ft.Page, contenedor_dinamico: ft.Container):
    """Construye la grilla de 11 tarjetas en orden de CATALOGO_BRIGADAS_BASE."""

    def _on_click_tarjeta(slug):
        def handler(e):
            contenedor_dinamico.content = _build_vista_guia(
                page, slug, mostrar_volver=True,
                on_volver=lambda: _volver_a_tarjetas(page, contenedor_dinamico),
            )
            page.update()
        return handler

    tarjetas = []
    for entrada in CATALOGO_BRIGADAS_BASE:
        slug = entrada["slug"]
        if slug not in CONTENIDO_EDUCATIVO:
            continue
        guia = CONTENIDO_EDUCATIVO[slug]
        color = _color_brigada(slug)
        color_osc = _color_brigada_oscuro(slug)
        nombre = _nombre_brigada(slug)
        icono = _icono(slug)

        resumen = guia.get("proposito", "")
        if len(resumen) > 130:
            resumen = resumen[:127] + "…"

        tarjeta = ft.Container(
            content=ft.Column(
                [
                    # Header con gradiente
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Icon(icono, color="white", size=32),
                                    width=56,
                                    height=56,
                                    border_radius=14,
                                    bgcolor=ft.Colors.with_opacity(0.25, "white"),
                                    alignment=ft.Alignment.CENTER,
                                ),
                                ft.Container(height=10),
                                ft.Text(nombre, size=15, weight="bold", color="white",
                                        max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                            ],
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                        padding=20,
                        border_radius=ft.BorderRadius.only(top_left=14, top_right=14),
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment.TOP_LEFT,
                            end=ft.Alignment.BOTTOM_RIGHT,
                            colors=[color, color_osc],
                        ),
                    ),
                    # Body
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(resumen, size=12, color=COLOR_TEXTO_SEC,
                                        max_lines=3, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Container(height=12),
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Text("Ver guía", size=13, weight="w600", color=color),
                                            ft.Icon(ft.Icons.ARROW_FORWARD, color=color, size=16),
                                        ],
                                        spacing=4,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    padding=ft.Padding(12, 8, 12, 8),
                                    border_radius=8,
                                    border=ft.Border.all(1.5, color),
                                    on_click=_on_click_tarjeta(slug),
                                ),
                            ],
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                        padding=16,
                        bgcolor=COLOR_CARD,
                        border_radius=ft.BorderRadius.only(bottom_left=14, bottom_right=14),
                        border=ft.Border(
                            left=ft.BorderSide(1, COLOR_BORDE),
                            bottom=ft.BorderSide(1, COLOR_BORDE),
                            right=ft.BorderSide(1, COLOR_BORDE),
                        ),
                    ),
                ],
                spacing=0,
            ),
            border_radius=14,
            shadow=get_sombra_suave(),
            on_click=_on_click_tarjeta(slug),
            width=300,
        )
        tarjetas.append(tarjeta)

    return ft.Column(
        [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.SCHOOL_OUTLINED, color=COLOR_PRIMARIO, size=28),
                        ft.Container(width=12),
                        ft.Column(
                            [
                                ft.Text("Contenido Educativo Institucional", size=18, weight="bold", color=COLOR_TEXTO),
                                ft.Text("Seleccione una brigada para consultar su guía completa.", size=14, color=COLOR_TEXTO_SEC),
                            ],
                            spacing=4,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding(0, 0, 0, 16),
            ),
            ft.Row(
                tarjetas,
                wrap=True,
                spacing=16,
                run_spacing=16,
                alignment=ft.MainAxisAlignment.START,
            ),
        ],
        spacing=0,
    )


def _volver_a_tarjetas(page: ft.Page, contenedor_dinamico: ft.Container):
    """Restaura la grilla de tarjetas sin modificar brigada_activa."""
    contenedor_dinamico.content = _build_grid_tarjetas(page, contenedor_dinamico)
    page.update()


# ─────────────────────────────────────────────────────────────
# VISTA DE GUÍA COMPLETA
# ─────────────────────────────────────────────────────────────
def _build_vista_guia(page: ft.Page, slug: str, mostrar_volver=False, on_volver=None):
    """Construye la vista completa de una guía educativa."""
    guia = CONTENIDO_EDUCATIVO.get(slug, {})
    color = _color_brigada(slug)
    color_osc = _color_brigada_oscuro(slug)
    nombre = _nombre_brigada(slug)
    icono = _icono(slug)

    secciones = []

    # Botón volver (solo para directivo)
    if mostrar_volver and on_volver:
        secciones.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ARROW_BACK, color=COLOR_PRIMARIO, size=18),
                        ft.Text("Volver a contenidos", size=14, weight="w500", color=COLOR_PRIMARIO),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.START,
                ),
                on_click=lambda e: on_volver(),
                padding=ft.Padding(0, 0, 0, 16),
            )
        )

    # Header con gradiente
    header = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(icono, color="white", size=48),
                    width=72,
                    height=72,
                    border_radius=16,
                    bgcolor=ft.Colors.with_opacity(0.2, "white"),
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Container(width=20),
                ft.Column(
                    [
                        ft.Text(nombre, size=22, weight="bold", color="white"),
                        ft.Text("Guía Operativa y Pedagógica", size=14,
                                color=ft.Colors.with_opacity(0.9, "white")),
                    ],
                    spacing=4,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=24,
        border_radius=ft.BorderRadius.only(top_left=16, top_right=16),
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[color, color_osc],
        ),
    )

    # Secciones de contenido
    body_items = []

    _agregar_seccion(body_items, ft.Icons.STARS_OUTLINED, "Propósito", guia.get("proposito"), color)
    _agregar_seccion(body_items, ft.Icons.BADGE_OUTLINED, "Identificación Visual", guia.get("identificacion"), color)
    _agregar_seccion(body_items, ft.Icons.FLAG_OUTLINED, "Misión de la Brigada", guia.get("mision"), color)
    _agregar_seccion(body_items, ft.Icons.GAVEL_OUTLINED, "Marco Orientador", guia.get("fundamento"), color)
    _agregar_seccion(body_items, ft.Icons.PERSON_OUTLINED, "Perfil del Brigadista", guia.get("perfil_brigadista"), color, es_lista=True)
    _agregar_seccion(body_items, ft.Icons.ASSIGNMENT_OUTLINED, "Funciones Principales", guia.get("funciones"), color, es_lista=True)
    _agregar_seccion(body_items, ft.Icons.FORMAT_LIST_NUMBERED, "Protocolo de Actuación", guia.get("protocolo"), color, es_lista=True)

    # Actividades pedagógicas (lista de dicts)
    actividades = guia.get("actividades_pedagogicas", [])
    if actividades:
        body_items.append(
            ft.Row(
                [ft.Icon(ft.Icons.LIGHTBULB_OUTLINED, color=color, size=20),
                 ft.Text("Actividades Pedagógicas Sugeridas", size=15, weight="w700", color=COLOR_TEXTO)],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        body_items.append(ft.Container(height=6))
        for act in actividades:
            body_items.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(act.get("nombre", ""), size=14, weight="w600", color=COLOR_TEXTO),
                            ft.Text(act.get("descripcion", ""), size=13, color=COLOR_TEXTO_SEC),
                        ],
                        spacing=2,
                    ),
                    padding=ft.Padding(12, 10, 12, 10),
                    border_radius=8,
                    bgcolor=ft.Colors.with_opacity(0.04, color),
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.15, color)),
                    margin=ft.margin.only(bottom=6),
                )
            )
        body_items.append(ft.Container(height=24))

    _agregar_seccion(body_items, ft.Icons.PHONE_IPHONE_OUTLINED, "Uso dentro de la Plataforma SBE", guia.get("uso_sbe"), color, es_lista=True)
    _agregar_seccion(body_items, ft.Icons.INSIGHTS_OUTLINED, "Indicadores y Evidencias", guia.get("indicadores"), color, es_lista=True)
    _agregar_seccion(body_items, ft.Icons.BLOCK_OUTLINED, "Límites de Actuación", guia.get("limites_actuacion"), color, es_lista=True)
    _agregar_seccion(body_items, ft.Icons.CHECKLIST_OUTLINED, "Lista de Chequeo Rápida", guia.get("checklist"), color, es_lista=True)

    body = ft.Container(
        content=ft.Column(body_items, spacing=0),
        padding=32,
        bgcolor=COLOR_CARD,
        border_radius=ft.BorderRadius.only(bottom_left=16, bottom_right=16),
        border=ft.Border(
            left=ft.BorderSide(1, COLOR_BORDE),
            bottom=ft.BorderSide(1, COLOR_BORDE),
            right=ft.BorderSide(1, COLOR_BORDE),
        ),
    )

    guia_card = ft.Container(
        content=ft.Column([header, body], spacing=0),
        border_radius=16,
        shadow=get_sombra_card(),
    )

    secciones.append(guia_card)
    secciones.append(ft.Container(height=32))

    return ft.Column(secciones, spacing=0)


def _agregar_seccion(items: list, icono, titulo: str, contenido, color: str, es_lista=False):
    """Agrega una sección con icono, título y contenido (texto o lista)."""
    if not contenido:
        return

    items.append(
        ft.Row(
            [ft.Icon(icono, color=color, size=20),
             ft.Text(titulo, size=15, weight="w700", color=COLOR_TEXTO)],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    items.append(ft.Container(height=6))

    if es_lista and isinstance(contenido, list):
        for item in contenido:
            items.append(
                ft.Row(
                    [
                        ft.Container(
                            width=6, height=6, border_radius=3,
                            bgcolor=color, margin=ft.margin.only(top=6, right=8),
                        ),
                        ft.Text(str(item), size=14, color=COLOR_TEXTO_SEC, expand=True),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                )
            )
            items.append(ft.Container(height=4))
    else:
        items.append(ft.Text(str(contenido), size=14, color=COLOR_TEXTO_SEC))

    items.append(ft.Container(height=24))


# ─────────────────────────────────────────────────────────────
# EMPTY STATES
# ─────────────────────────────────────────────────────────────
def _build_empty_state_sin_brigada():
    """Profesor sin brigada asignada."""
    return ft.Container(
        content=card_principal(
            ft.Column(
                [
                    ft.Icon(ft.Icons.SCHOOL_OUTLINED, color=COLOR_TEXTO_SEC, size=64),
                    ft.Container(height=16),
                    ft.Text("Sin brigada asignada", size=20, weight="bold", color=COLOR_TEXTO),
                    ft.Container(height=8),
                    ft.Text(
                        "No posee una brigada asignada. Solicite a la dirección institucional "
                        "la asignación correspondiente para acceder al contenido educativo específico.",
                        size=14, color=COLOR_TEXTO_SEC,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
        ),
        padding=32,
        alignment=ft.Alignment(0, 0),
    )


def _build_empty_state_sin_acceso(error_msg=None):
    """Directivo sin institucion_id o error de contexto."""
    return ft.Container(
        content=card_principal(
            ft.Column(
                [
                    ft.Icon(ft.Icons.LOCK_OUTLINED, color=COLOR_TEXTO_SEC, size=64),
                    ft.Container(height=16),
                    ft.Text("Acceso no disponible", size=20, weight="bold", color=COLOR_TEXTO),
                    ft.Container(height=8),
                    ft.Text(
                        error_msg or "No se pudo determinar el contexto de acceso. "
                        "Verifique su sesión e intente nuevamente.",
                        size=14, color=COLOR_TEXTO_SEC,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
        ),
        padding=32,
        alignment=ft.Alignment(0, 0),
    )


def _build_empty_contenido(tipo_brigada=None):
    """Profesor con brigada pero sin contenido educativo disponible para ese tipo."""
    return ft.Container(
        content=card_principal(
            ft.Column(
                [
                    ft.Icon(ft.Icons.INFO_OUTLINE, color=COLOR_PRIMARIO, size=48),
                    ft.Container(height=16),
                    ft.Text(
                        f"Contenido educativo no disponible para la brigada tipo '{tipo_brigada or 'desconocido'}'.",
                        size=16, color=COLOR_TEXTO_SEC,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
        ),
        padding=32,
        alignment=ft.Alignment(0, 0),
    )
