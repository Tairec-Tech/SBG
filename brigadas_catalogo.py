"""
Catálogo oficial de las 11 brigadas escolares base (Ministerio de Educación).

Módulo neutral — SIN dependencias de UI/Flet.
Usado por la capa de datos (crud_usuario, crud_brigada) para la creación
automática de brigadas al registrar una institución.
theme.py mantiene sus propias paletas/temas pero debe estar alineado con estos slugs.
"""

CATALOGO_BRIGADAS_BASE = [
    {
        "slug": "ecologica",
        "nombre": "Brigada Ecológica",
        "tipo_brigada": "ecologica",
        "area_accion": "Medio Ambiente",
        "descripcion": "Reciclaje, conservación ambiental, ahorro de recursos y cuidado de áreas verdes.",
        "color": "#059669",
    },
    {
        "slug": "riesgo",
        "nombre": "Brigada de Gestión de Riesgo",
        "tipo_brigada": "riesgo",
        "area_accion": "Prevención y Emergencias",
        "descripcion": "Prevención, identificación de amenazas, simulacros, evacuación y respuesta organizada ante emergencias.",
        "color": "#ea580c",
    },
    {
        "slug": "patrulla",
        "nombre": "Brigada de Patrulla Escolar",
        "tipo_brigada": "patrulla",
        "area_accion": "Seguridad Vial",
        "descripcion": "Seguridad vial, control peatonal, orden en entradas y salidas y cultura vial escolar.",
        "color": "#dc2626",
    },
    {
        "slug": "convivencia",
        "nombre": "Brigada de Convivencia y Paz",
        "tipo_brigada": "convivencia",
        "area_accion": "Mediación y Respeto",
        "descripcion": "Mediación, respeto, tolerancia, prevención de violencia, hostigamiento y conflictos escolares.",
        "color": "#64748b",
    },
    {
        "slug": "auxilios",
        "nombre": "Brigada de Primeros Auxilios",
        "tipo_brigada": "auxilios",
        "area_accion": "Salud Escolar",
        "descripcion": "Atención inmediata básica, prevención de salud escolar y apoyo inicial ante accidentes o lesiones.",
        "color": "#eab308",
    },
    {
        "slug": "educacion_fisica",
        "nombre": "Brigada de Educación Física",
        "tipo_brigada": "educacion_fisica",
        "area_accion": "Recreación y Deporte",
        "descripcion": "Actividad física, recreación, hábitos saludables y apoyo a jornadas deportivas escolares.",
        "color": "#3b82f6",
    },
    {
        "slug": "conuco",
        "nombre": "Brigada Mi Conuco Escolar",
        "tipo_brigada": "conuco",
        "area_accion": "Soberanía Alimentaria",
        "descripcion": "Huertos y conucos escolares, producción pedagógica y soberanía alimentaria.",
        "color": "#84cc16",
    },
    {
        "slug": "patrimonio",
        "nombre": "Brigada de Patrimonio y Turismo",
        "tipo_brigada": "patrimonio",
        "area_accion": "Identidad Cultural",
        "descripcion": "Valoración del patrimonio histórico-cultural, identidad local y reconocimiento del entorno.",
        "color": "#ec4899",
    },
    {
        "slug": "artes",
        "nombre": "Brigada de Artes Visuales",
        "tipo_brigada": "artes",
        "area_accion": "Expresión Artística",
        "descripcion": "Murales, carteleras, exposiciones y apoyo visual a actividades escolares.",
        "color": "#a855f7",
    },
    {
        "slug": "patriotica",
        "nombre": "Brigada Juventud Patriótica",
        "tipo_brigada": "patriotica",
        "area_accion": "Identidad Nacional",
        "descripcion": "Símbolos patrios, efemérides, memoria histórica e identidad nacional.",
        "color": "#9ca3af",
    },
    {
        "slug": "ddhh",
        "nombre": "Brigada de Derechos Humanos",
        "tipo_brigada": "ddhh",
        "area_accion": "Dignidad e Inclusión",
        "descripcion": "Dignidad, igualdad, inclusión, trato justo y prevención de vulneraciones.",
        "color": "#1e3a8a",
    },
]
