# Inicio aporte Mathias Giler (matheoglg): conexión de la interfaz con los analizadores
# La interfaz no analiza nada por su cuenta: llama al lexer, al parser y a la parte
# semántica que ya existen en src/, y devuelve los resultados en un formato fácil de mostrar.
import os
from datetime import datetime

from lexer_dart import lexer, errors as errores_lexicos, reserved
from parser_dart import parser, errores_sintacticos, errores_semanticos, reiniciar_semantico

FASES = ("lexico", "sintactico", "semantico")
NOMBRE_FASE = {"lexico": "Léxico", "sintactico": "Sintáctico", "semantico": "Semántico"}

# Carpeta logs/ en la raíz del repositorio (src/interfaz/ -> raíz)
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CARPETA_LOGS = os.path.join(RAIZ, "logs")

LITERALES = {"ENTERO", "DECIMAL", "CADENA", "TRUE", "FALSE", "NULL"}
OPERADORES = {"SUMA", "RESTA", "MULTIPLICACION", "DIVISION", "DIV_ENTERA", "MODULO",
              "INCREMENTO", "DECREMENTO", "FLECHA", "MENOR_QUE", "MAYOR_QUE", "MENOR_IGUAL",
              "MAYOR_IGUAL", "IGUAL", "DIFERENTE", "NOT", "AND", "OR", "ASIGNACION",
              "ASIGNACION_NULL"}
PALABRAS = set(reserved.values())


def categoria(tipo):
    """Agrupa los tokens en las 5 categorías de la leyenda del prototipo."""
    if tipo in LITERALES:
        return "Literal"
    if tipo == "ID":
        return "Identificador"
    if tipo in OPERADORES:
        return "Operador"
    if tipo in PALABRAS:
        return "Reservada"
    return "Delimitador"


def _preparar():
    lexer.lineno = 1
    errores_lexicos.clear()
    errores_sintacticos.clear()
    reiniciar_semantico()


def analizar_lexico(codigo):
    _preparar()
    lexer.input(codigo)
    tokens = []
    for tok in lexer:
        tokens.append((tok.lineno, tok.type, str(tok.value), categoria(tok.type)))
    errores = [(linea, "Léxico", f"carácter '{car}' no reconocido")
               for linea, car in errores_lexicos]
    return {"fase": "lexico", "tokens": tokens, "errores": errores}


def analizar_sintactico(codigo):
    _preparar()
    parser.parse(codigo, lexer=lexer)
    errores = []
    for linea, msg in errores_sintacticos:
        errores.append((linea, "Sintáctico", msg))
    return {"fase": "sintactico", "errores": errores}


def analizar_semantico(codigo):
    # El análisis semántico se hace mientras el parser reconoce cada regla,
    # por eso se vuelve a parsear el código y se leen los errores semánticos.
    _preparar()
    parser.parse(codigo, lexer=lexer)
    errores = [(linea, f"Semántico · {cat}", msg) for linea, cat, msg in errores_semanticos]
    return {"fase": "semantico", "errores": errores,
            "aviso_sintaxis": len(errores_sintacticos)}


ANALIZAR = {"lexico": analizar_lexico, "sintactico": analizar_sintactico,
            "semantico": analizar_semantico}


def texto_log(resultado, archivo, usuario):
    """Arma el contenido del log con el mismo formato que los ejecutores de consola."""
    fase = resultado["fase"]
    lineas = [f"Archivo: {archivo}", f"Usuario: {usuario}", ""]
    errores = resultado["errores"]
    if fase == "lexico":
        for linea, tipo, valor, _ in resultado["tokens"]:
            lineas.append(f"L{linea:>3}  {tipo:<15} {valor!r}")
        lineas.append("")
        lineas.append(f"Errores léxicos: {len(errores)}")
        for linea, _, msg in errores:
            lineas.append(f"  Línea {linea}: {msg}")
    elif fase == "sintactico":
        for linea, _, msg in errores:
            if linea is None:
                lineas.append(f"Error de sintaxis: {msg}")
            else:
                lineas.append(f"Error de sintaxis en línea {linea}: {msg}")
        if not errores:
            lineas.append("No se encontraron errores sintácticos.")
        lineas.append("")
        lineas.append(f"Errores sintácticos: {len(errores)}")
    else:
        if resultado.get("aviso_sintaxis"):
            lineas.append(f"Aviso: el código tiene {resultado['aviso_sintaxis']} error(es) "
                          "sintáctico(s), el análisis semántico puede estar incompleto.")
            lineas.append("")
        for linea, cat, msg in errores:
            cat = cat.replace("Semántico · ", "")
            lineas.append(f"Error semántico ({cat}) en línea {linea}: {msg}")
        if not errores:
            lineas.append("No se encontraron errores semánticos.")
        lineas.append("")
        lineas.append(f"Errores semánticos: {len(errores)}")
    return "\n".join(lineas) + "\n"


def nombre_log(fase, usuario, momento=None):
    momento = momento or datetime.now()
    return f"{fase}-{usuario}-{momento.strftime('%d-%m-%Y-%Hh%M')}.txt"


def guardar_log(nombre, contenido):
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    ruta = os.path.join(CARPETA_LOGS, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta
# Fin aporte Mathias Giler
