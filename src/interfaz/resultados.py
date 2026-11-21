# Inicio aporte Marcia Torres (marciatorresg): panel de resultados
# Pestañas Tokens y Errores: tabla de tokens con colores por categoría, progreso de las
# fases y lista de errores; al seleccionar un error se resalta su línea en el editor.
import tkinter as tk
from tkinter import ttk

from interfaz import tema
from interfaz.analizador import FASES, NOMBRE_FASE


class PanelResultados(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=tema.BLANCO)
        self.app = app
        self.errores = []
        self.pestanas = ttk.Notebook(self)
        self.pestanas.pack(fill="both", expand=True)

        self.tab_tokens = tk.Frame(self.pestanas, bg=tema.BLANCO)
        self.tab_errores = tk.Frame(self.pestanas, bg=tema.BLANCO)
        self.pestanas.add(self.tab_tokens, text="Tokens")
        self.pestanas.add(self.tab_errores, text="Errores")
        self._crear_pestana_tokens()
        self._crear_pestana_errores()
        # Pestaña Log (Marcia Torres, commit 2)
        self.limpiar()

    # ------------------------------------------------------------------ pestaña Tokens
    def _crear_pestana_tokens(self):
        f = self.app.f
        self.resumen = tk.Frame(self.tab_tokens, bg=tema.FONDO, padx=14, pady=10)
        self.resumen.pack(fill="x")
        self.resumen_icono = tk.Label(self.resumen, text="i", width=2, font=f["negrita"])
        self.resumen_icono.pack(side="left", padx=(0, 10))
        textos = tk.Frame(self.resumen, bg=tema.FONDO)
        textos.pack(side="left", fill="x")
        self.resumen_titulo = tk.Label(textos, font=f["negrita"], anchor="w")
        self.resumen_titulo.pack(fill="x")
        self.resumen_detalle = tk.Label(textos, font=f["pequena"], anchor="w")
        self.resumen_detalle.pack(fill="x")

        progreso = tk.Frame(self.tab_tokens, bg="#fbfcfd", padx=14, pady=9)
        progreso.pack(fill="x")
        self.cajas_fase = {}
        for i, fase in enumerate(FASES):
            caja = tk.Frame(progreso, bg=tema.BLANCO, highlightthickness=1, padx=8, pady=6)
            caja.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 8, 0))
            progreso.columnconfigure(i, weight=1)
            numero = tk.Label(caja, text=str(i + 1), width=2, font=f["negrita"])
            numero.pack(side="left", padx=(0, 8))
            nombre = tk.Label(caja, text=NOMBRE_FASE[fase], font=f["negrita"], anchor="w")
            nombre.pack(anchor="w")
            estado = tk.Label(caja, text="Pendiente", font=f["pequena"], anchor="w")
            estado.pack(anchor="w")
            self.cajas_fase[fase] = (caja, numero, nombre, estado)

        leyenda = tk.Frame(self.tab_tokens, bg=tema.BLANCO, padx=14, pady=7)
        leyenda.pack(fill="x")
        for cat, (color, _) in tema.COLOR_CATEGORIA.items():
            tk.Label(leyenda, text="●", fg=color, bg=tema.BLANCO, font=f["pequena"]).pack(side="left")
            tk.Label(leyenda, text=cat, fg=tema.TEXTO_SUAVE, bg=tema.BLANCO,
                     font=f["pequena"]).pack(side="left", padx=(2, 12))

        tabla = tk.Frame(self.tab_tokens, bg=tema.BLANCO)
        tabla.pack(fill="both", expand=True)
        columnas = ("linea", "token", "valor", "categoria")
        self.tabla_tokens = ttk.Treeview(tabla, columns=columnas, show="headings")
        for col, titulo, ancho in (("linea", "LÍNEA", 60), ("token", "TOKEN", 170),
                                   ("valor", "VALOR", 170), ("categoria", "CATEGORÍA", 110)):
            self.tabla_tokens.heading(col, text=titulo, anchor="w")
            self.tabla_tokens.column(col, width=ancho, anchor="w", stretch=col != "linea")
        for cat, (color, fondo) in tema.COLOR_CATEGORIA.items():
            self.tabla_tokens.tag_configure(cat, foreground=color, background=fondo)
        barra = ttk.Scrollbar(tabla, orient="vertical", command=self.tabla_tokens.yview)
        self.tabla_tokens.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        self.tabla_tokens.pack(side="left", fill="both", expand=True)

    def _poner_resumen(self, tono, titulo, detalle):
        colores = {"exito": (tema.EXITO_SUAVE, tema.EXITO, "#225e26", "✓"),
                   "error": (tema.ERROR_SUAVE, tema.ERROR, tema.ERROR, "!"),
                   "neutro": (tema.AZUL_SUAVE, tema.AZUL, tema.TEXTO, "i")}
        fondo, marca, texto, icono = colores[tono]
        for w in (self.resumen, self.resumen_titulo.master, self.resumen_titulo, self.resumen_detalle):
            w.configure(bg=fondo)
        self.resumen_icono.configure(text=icono, bg=marca, fg=tema.BLANCO)
        self.resumen_titulo.configure(text=titulo, fg=texto)
        self.resumen_detalle.configure(text=detalle, fg=tema.TEXTO_SUAVE)

    def _pintar_fase(self, fase, estado):
        caja, numero, nombre, texto = self.cajas_fase[fase]
        estilos = {"correcto": (tema.EXITO_SUAVE, "#b9d8bb", tema.EXITO, "✓", "Correcto"),
                   "error": (tema.ERROR_SUAVE, "#f0c9c9", tema.ERROR, "!", "Con errores"),
                   "siguiente": (tema.AZUL_SUAVE, "#9dcde9", tema.AZUL, None, "Siguiente fase"),
                   "pendiente": (tema.BLANCO, tema.LINEA, tema.DESHABILITADO, None, "Pendiente")}
        fondo, borde, color, icono, etiqueta = estilos[estado]
        caja.configure(bg=fondo, highlightbackground=borde)
        numero.configure(text=icono or str(FASES.index(fase) + 1), bg=color, fg=tema.BLANCO)
        nombre.configure(bg=fondo, fg=color if estado != "pendiente" else tema.TEXTO_SUAVE)
        texto.configure(text=etiqueta, bg=fondo, fg=color)

    # ------------------------------------------------------------------ pestaña Errores
    def _crear_pestana_errores(self):
        f = self.app.f
        self.cabecera_errores = tk.Label(self.tab_errores, anchor="w", padx=14, pady=12,
                                         font=f["negrita"])
        self.cabecera_errores.pack(fill="x")
        tabla = tk.Frame(self.tab_errores, bg=tema.BLANCO)
        tabla.pack(fill="both", expand=True, padx=10, pady=10)
        columnas = ("categoria", "linea", "mensaje")
        self.tabla_errores = ttk.Treeview(tabla, columns=columnas, show="headings",
                                          selectmode="browse")
        for col, titulo, ancho in (("categoria", "FASE / CATEGORÍA", 280), ("linea", "LÍNEA", 55),
                                   ("mensaje", "MENSAJE", 640)):
            self.tabla_errores.heading(col, text=titulo, anchor="w")
            self.tabla_errores.column(col, width=ancho, minwidth=ancho, anchor="w",
                                      stretch=col == "mensaje")
        self.tabla_errores.tag_configure("error", foreground=tema.ERROR)
        barra = ttk.Scrollbar(tabla, orient="vertical", command=self.tabla_errores.yview)
        barra_h = ttk.Scrollbar(tabla, orient="horizontal", command=self.tabla_errores.xview)
        self.tabla_errores.configure(yscrollcommand=barra.set, xscrollcommand=barra_h.set)
        barra.pack(side="right", fill="y")
        barra_h.pack(side="bottom", fill="x")
        self.tabla_errores.pack(side="left", fill="both", expand=True)
        # Mensaje completo del error seleccionado, por si es más largo que la tabla
        self.detalle_error = tk.Label(self.tab_errores, text="", bg=tema.BLANCO, fg="#344054",
                                      font=f["normal"], anchor="w", justify="left",
                                      wraplength=560, padx=14, pady=8)
        self.detalle_error.pack(fill="x")
        self.tabla_errores.bind("<<TreeviewSelect>>", self._al_elegir_error)

    def _al_elegir_error(self, _evento=None):
        seleccion = self.tabla_errores.selection()
        if seleccion:
            linea, cat, msg = self.errores[self.tabla_errores.index(seleccion[0])]
            self.detalle_error.configure(text=f"{cat} · línea {linea}: {msg}")
            self.app.ir_a_linea(linea)

    def seleccionar_error(self, indice):
        filas = self.tabla_errores.get_children()
        if 0 <= indice < len(filas):
            self.pestanas.select(self.tab_errores)
            self.tabla_errores.selection_set(filas[indice])
            self.tabla_errores.see(filas[indice])

    # ------------------------------------------------------------------ actualizar todo
    def limpiar(self):
        self.mostrar({})

    def mostrar(self, sesion):
        # Tabla de tokens
        self.tabla_tokens.delete(*self.tabla_tokens.get_children())
        if "lexico" in sesion:
            for linea, tipo, valor, cat in sesion["lexico"]["tokens"]:
                self.tabla_tokens.insert("", "end", values=(linea, tipo, valor, cat), tags=(cat,))

        # Progreso de las fases y resumen
        ejecutadas = [f for f in FASES if f in sesion]
        con_error = next((f for f in ejecutadas if sesion[f]["errores"]), None)
        for i, fase in enumerate(FASES):
            if fase in sesion:
                self._pintar_fase(fase, "error" if sesion[fase]["errores"] else "correcto")
            elif con_error is None and i == len(ejecutadas):
                self._pintar_fase(fase, "siguiente")
            else:
                self._pintar_fase(fase, "pendiente")

        if not ejecutadas:
            self._poner_resumen("neutro", "Aún no hay resultados",
                                "Escribe o carga código Dart y elige una fase para analizar.")
        elif con_error:
            n = len(sesion[con_error]["errores"])
            self._poner_resumen("error", f"El análisis {NOMBRE_FASE[con_error].lower()} encontró "
                                         f"{n} error{'es' if n != 1 else ''}",
                                "Revisa la pestaña Errores. La siguiente fase queda bloqueada "
                                "hasta corregirlo.")
        elif len(ejecutadas) == 3:
            total = len(sesion["lexico"]["tokens"])
            self._poner_resumen("exito", "Caso válido · análisis completo",
                                f"Las 3 fases finalizaron correctamente · {total} tokens · 0 errores")
        else:
            self._poner_resumen("exito", f"Fase {len(ejecutadas)} de 3 completada",
                                "El código es válido hasta la fase analizada · 0 errores")

        # Lista de errores
        self.errores = [e for f in ejecutadas for e in sesion[f]["errores"]]
        self.tabla_errores.delete(*self.tabla_errores.get_children())
        self.detalle_error.configure(text="")
        for linea, cat, msg in self.errores:
            self.tabla_errores.insert("", "end", values=(cat, linea if linea else "—", msg),
                                      tags=("error",))
        n = len(self.errores)
        self.pestanas.tab(self.tab_errores, text=f"Errores ({n})" if n else "Errores")
        if n:
            self.cabecera_errores.configure(
                text=f"⚠  {n} {'error encontrado' if n == 1 else 'errores encontrados'}"
                     "   ·   Selecciona un error para ir a la línea",
                bg=tema.ERROR_SUAVE, fg=tema.ERROR)
            self.pestanas.select(self.tab_errores)
        else:
            self.cabecera_errores.configure(
                text="✓  No hay errores que mostrar. Los errores de cada fase aparecerán aquí "
                     "con su línea y categoría.", bg=tema.EXITO_SUAVE, fg=tema.EXITO)
            self.pestanas.select(self.tab_tokens)
        # Actualizar log (Marcia Torres, commit 2)
# Fin aporte Marcia Torres
