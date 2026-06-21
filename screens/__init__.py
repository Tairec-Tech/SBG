# Pantallas del SBE — diseño Figma, brigadas ambientales (verde)

import importlib

def __getattr__(name):
    """Lazy import: solo carga el módulo cuando se accede."""
    if name in __all__:
        return importlib.import_module(f".{name}", __name__)
    raise AttributeError(f"module 'screens' has no attribute {name}")

__all__ = [
    "screen_dashboard",
    "screen_brigades",
    "screen_brigadistas",
    "screen_activities",
    "screen_shifts",
    "screen_reports",
    "screen_reports_impact",
    "screen_reports_activities",
    "screen_statistics",
    "screen_content",
    "screen_login",
    "screen_register",
    "screen_recovery",
    "screen_about",
    "screen_manual",
    "screen_legal",
    "screen_backup",
    "screen_utilidades",
    "screen_brigade_select",
]

