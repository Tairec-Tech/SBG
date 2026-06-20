import flet as ft
import os
from theme import COLOR_PRIMARIO, COLOR_TEXTO, COLOR_TEXTO_SEC, COLOR_BORDE, COLOR_CARD, RADIO
from database.crud_reporte import obtener_media_reporte

def abrir_modal_detalle_reporte(page: ft.Page, reporte: dict, tipo: str, fn_descargar):
    """
    Muestra un modal estilo Jira con los detalles del reporte a la izquierda
    y la galería multimedia (imágenes/videos) a la derecha.
    """
    id_entidad = reporte.get("id")
    # Obtener archivos
    archivos = obtener_media_reporte(tipo, id_entidad)
    imagenes = [m for m in archivos if m["tipo"] == "imagen"]
    videos = [m for m in archivos if m["tipo"] == "video"]
    
    # ==========================
    # PANEL IZQUIERDO: DETALLES
    # ==========================
    detalles_col = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)
    
    def _add_texto(titulo, valor):
        if valor:
            detalles_col.controls.append(ft.Column([
                ft.Text(titulo, size=13, weight="w600", color=COLOR_TEXTO_SEC),
                ft.Text(str(valor), size=14, color=COLOR_TEXTO)
            ], spacing=2))

    if tipo == "impacto":
        _add_texto("ID Evaluación", f"IMP-{id_entidad}")
        _add_texto("Fecha de Evaluación", reporte.get("fecha_generacion"))
        _add_texto("Evaluador", reporte.get("usuario_nombre"))
        _add_texto("Brigada", reporte.get("brigada"))
        _add_texto("Área Evaluada", reporte.get("area_evaluada"))
        
        ind_txt = reporte.get("indicador", "")
        if reporte.get("valor"): ind_txt += f": {reporte.get('valor')}"
        if reporte.get("unidad"): ind_txt += f" {reporte.get('unidad')}"
        _add_texto("Indicador", ind_txt)
        
        _add_texto("Descripción del Impacto", reporte.get("contenido"))
        _add_texto("Actividad Asociada", reporte.get("actividad_titulo"))
        
    elif tipo == "actividad":
        _add_texto("ID Reporte", f"ACT-{id_entidad}")
        _add_texto("Fecha de Emisión", reporte.get("fecha_reporte"))
        _add_texto("Reportado Por", reporte.get("usuario_nombre"))
        _add_texto("Actividad", reporte.get("actividad_titulo"))
        _add_texto("Fecha de Ejecución", reporte.get("actividad_fecha"))
        _add_texto("Resultado General", reporte.get("resultado"))
        _add_texto("Participantes", reporte.get("participantes"))
        _add_texto("Observaciones", reporte.get("resumen"))

    # ==========================
    # PANEL DERECHO: MULTIMEDIA
    # ==========================
    media_col = ft.Column(spacing=16, scroll=ft.ScrollMode.AUTO, expand=True)
    
    if not imagenes and not videos:
        media_col.controls.append(
            ft.Container(
                content=ft.Text("Sin archivos adjuntos.", color=COLOR_TEXTO_SEC, italic=True),
                padding=20, alignment=ft.Alignment(0, 0)
            )
        )
    else:
        if imagenes:
            media_col.controls.append(ft.Text("Imágenes Adjuntas", size=14, weight="bold", color=COLOR_TEXTO))
            grid_img = ft.Row(wrap=True, spacing=10)
            for img in imagenes:
                # Usar src con la ruta absoluta si es un archivo local
                abs_path = os.path.abspath(img["ruta"])
                grid_img.controls.append(
                    ft.Image(
                        src=abs_path,
                        width=150, height=150,
                        fit="cover",
                        border_radius=RADIO
                    )
                )
            media_col.controls.append(grid_img)
            
        if videos:
            media_col.controls.append(ft.Text("Videos Adjuntos", size=14, weight="bold", color=COLOR_TEXTO))
            for vid in videos:
                abs_path = os.path.abspath(vid["ruta"])
                # No existe ft.Video por defecto en esta versión, así que usamos un botón nativo
                def on_open_video(e, path=abs_path):
                    import os, platform, subprocess
                    if platform.system() == 'Windows':
                        os.startfile(path)
                    elif platform.system() == 'Darwin':
                        subprocess.call(('open', path))
                    else:
                        subprocess.call(('xdg-open', path))
                        
                video_card = ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.VIDEO_FILE, color=ft.Colors.RED, size=40),
                        ft.Column([
                            ft.Text(os.path.basename(abs_path), size=14, weight="w500", color=COLOR_TEXTO),
                            ft.ElevatedButton("Abrir en reproductor", icon=ft.Icons.PLAY_ARROW, on_click=on_open_video, style=ft.ButtonStyle(color=COLOR_PRIMARIO))
                        ], spacing=4)
                    ]),
                    padding=12,
                    bgcolor=ft.Colors.with_opacity(0.05, COLOR_TEXTO),
                    border_radius=RADIO,
                    border=ft.Border.all(1, COLOR_BORDE)
                )
                media_col.controls.append(video_card)

    # ==========================
    # CONSTRUCCIÓN DEL MODAL
    # ==========================
    
    def on_descargar(e):
        page.run_task(fn_descargar, reporte)
    
    # Si hay videos, mostrar advertencia sobre el DOCX
    adv_video = ft.Text("Nota: Los videos no se incluyen en el DOCX.", size=11, color=ft.Colors.ORANGE, italic=True) if videos else ft.Container()
    
    btn_descargar = ft.Column([
        ft.ElevatedButton("Descargar DOCX", icon=ft.Icons.DOWNLOAD, on_click=on_descargar, style=ft.ButtonStyle(color=COLOR_PRIMARIO)),
        adv_video
    ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.END)

    content_row = ft.Row(
        [
            # Columna izquierda
            ft.Container(
                content=detalles_col,
                expand=2,
                padding=ft.padding.only(right=16),
                border=ft.border.only(right=ft.border.BorderSide(1, COLOR_BORDE))
            ),
            # Columna derecha
            ft.Container(
                content=media_col,
                expand=3,
                padding=ft.padding.only(left=16)
            )
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    dialogo = ft.AlertDialog(
        modal=False,
        bgcolor=COLOR_CARD,
        title=ft.Row([
            ft.Text("Detalle del Reporte", size=20, weight="bold", color=COLOR_TEXTO),
            ft.Container(expand=True),
            btn_descargar
        ]),
        content=ft.Container(
            content=content_row,
            width=900,
            height=500,
            bgcolor=COLOR_CARD
        ),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda _: page.pop_dialog(), style=ft.ButtonStyle(color=COLOR_TEXTO))
        ]
    )
    
    page.show_dialog(dialogo)
