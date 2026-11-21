# Inicio aporte Mathias Giler (matheoglg): colores y fuentes de la interfaz
# Los colores salen del prototipo DartLens hecho en Figma
import tkinter.font as tkfont

AZUL = "#0175c2"
AZUL_OSCURO = "#02569b"
CIAN = "#13b9fd"
AZUL_SUAVE = "#eaf6fd"
TEXTO = "#1d2939"
TEXTO_SUAVE = "#667085"
LINEA = "#d9e1e8"
LINEA_SUAVE = "#e9eef2"
BLANCO = "#ffffff"
FONDO = "#f4f7f9"
ERROR = "#d32f2f"
ERROR_SUAVE = "#fff0f0"
EXITO = "#2e7d32"
EXITO_SUAVE = "#edf7ee"
DESHABILITADO = "#98a2ad"

# Color de cada categoría de token (leyenda de la pestaña Tokens)
COLOR_CATEGORIA = {
    "Reservada": ("#015c99", "#e8f4fc"),
    "Identificador": ("#613795", "#f3edfa"),
    "Operador": ("#a75904", "#fff5e6"),
    "Literal": ("#236527", "#edf7ee"),
    "Delimitador": ("#475467", "#f0f2f4"),
}

# Integrantes del grupo y su usuario de GitHub (se usa en el nombre de los logs)
DESARROLLADORES = {
    "Juan Ayala": "JuanAyala619",
    "Marcia Torres": "marciatorresg",
    "Mathias Giler": "matheoglg",
}


def _primera_disponible(opciones, defecto):
    disponibles = set(tkfont.families())
    for nombre in opciones:
        if nombre in disponibles:
            return nombre
    return defecto


def fuentes():
    """Devuelve las fuentes a usar. Se llama después de crear la ventana."""
    ui = _primera_disponible(["Montserrat", "Segoe UI", "Helvetica Neue", "Arial"], "TkDefaultFont")
    mono = _primera_disponible(["JetBrains Mono", "Consolas", "Menlo", "DejaVu Sans Mono", "Courier New"],
                               "TkFixedFont")
    return {
        "titulo": (ui, 16, "bold"),
        "subtitulo": (ui, 8),
        "normal": (ui, 9),
        "negrita": (ui, 9, "bold"),
        "pequena": (ui, 8),
        "codigo": (mono, 11),
        "codigo_peq": (mono, 9),
    }
# Fin aporte Mathias Giler
