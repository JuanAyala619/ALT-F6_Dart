# ALT-F6_Dart

Analizador léxico, sintáctico y semántico de un subconjunto de **Dart**, hecho en Python con PLY, con una interfaz gráfica (DartLens) en Tkinter.

Proyecto de Lenguajes de Programación (ESPOL) — Grupo ALT-F6: Juan Ayala (JuanAyala619), Marcia Torres (marciatorresg) y Mathias Giler (matheoglg).

## Requisitos

- Python 3.10 o superior, con Tkinter (viene con el instalador oficial de Python en Windows y macOS; en Linux: `sudo apt install python3-tk`).
- PLY: `pip install -r requirements.txt`

## Interfaz gráfica (DartLens)

Desde la raíz del repositorio:

```
python src/dartlens.py
```

1. Elige tu nombre en **Desarrollador** (se usa para el nombre de los logs).
2. Escribe código Dart en el editor o usa **Cargar algoritmo de prueba (.dart)**.
3. Ejecuta las fases en orden: **Analizar léxico → sintáctico → semántico**, o **Ejecutar las 3 fases**. Una fase se habilita solo cuando la anterior terminó sin errores.
4. Revisa los resultados en las pestañas **Tokens**, **Errores** (al seleccionar un error se resalta su línea en el editor) y **Log**.
5. En la pestaña **Log**, **Guardar log** crea un archivo por fase ejecutada en `logs/` con el formato `lexico-usuarioGit-dd-mm-aaaa-HHhMM.txt` (igual para `sintactico-` y `semantico-`).

## Ejecutores por consola

```
python src/ejecucion_lexer.py algoritmos/<archivo>.dart <usuarioGit>
python src/ejecucion_parser.py algoritmos/<archivo>.dart <usuarioGit>
python src/ejecucion_semantico.py algoritmos/<archivo>.dart <usuarioGit>
```

## Estructura

```
src/
  lexer_dart.py          analizador léxico (PLY lex)
  parser_dart.py         analizador sintáctico y semántico (PLY yacc)
  ejecucion_*.py         ejecutores por consola que generan los logs
  dartlens.py            punto de entrada de la interfaz
  interfaz/
    tema.py              colores y fuentes (prototipo de Figma)
    analizador.py        conexión de la interfaz con los analizadores y logs
    app.py               ventana principal y barra de estado
    editor.py            editor con números de línea y carga de archivos
    controles.py         fases de análisis en orden
    resultados.py        pestañas Tokens y Errores
    pestana_log.py       pestaña Log y diálogo para guardar
algoritmos/              algoritmos de prueba de cada integrante
logs/                    logs de las pruebas
```
