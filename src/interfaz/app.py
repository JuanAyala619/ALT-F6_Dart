# Inicio aporte Mathias Giler (matheoglg): ventana principal de DartLens
# Arma la estructura de la ventana según el prototipo de Figma: barra superior,
# área de trabajo (editor y fases a la izquierda, resultados a la derecha) y barra de estado.
# Los componentes de cada integrante se agregan en _crear_componentes().
import tkinter as tk
from tkinter import ttk

from interfaz import tema
from interfaz.analizador import FASES, NOMBRE_FASE


class DartLens(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DartLens - Analizador de código Dart")
        self.geometry("1280x800")
        self.minsize(1100, 700)
        self.configure(bg=tema.FONDO)
        self.f = tema.fuentes()
        self._configurar_estilos()

        self.desarrollador = tk.StringVar(value="Mathias Giler")
        self.desarrollador.trace_add("write", lambda *_: self._al_cambiar_desarrollador())
        self.ultimo_log = tk.StringVar(value="—")
        self.archivo_actual = "algoritmo.dart"
        self.sesion = {}          # resultado de cada fase ejecutada: {"lexico": {...}, ...}

        # Componentes de cada integrante (se crean en _crear_componentes)
        self.editor = None
        self.controles = None
        self.resultados = None

        self._crear_barra_superior()
        self._crear_area_trabajo()
        self._crear_barra_estado()
        self._crear_componentes()
        self.actualizar_estado()

    # ------------------------------------------------------------------ estilos
    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TNotebook", background=tema.BLANCO, borderwidth=0)
        estilo.configure("TNotebook.Tab", font=self.f["negrita"], padding=(16, 8),
                         background="#fafcfd", foreground=tema.TEXTO_SUAVE, borderwidth=0)
        estilo.map("TNotebook.Tab", background=[("selected", tema.BLANCO)],
                   foreground=[("selected", tema.AZUL_OSCURO)])
        estilo.configure("Treeview", font=self.f["codigo_peq"], rowheight=26,
                         background=tema.BLANCO, fieldbackground=tema.BLANCO, borderwidth=0)
        estilo.configure("Treeview.Heading", font=self.f["pequena"], background="#f5f7f9",
                         foreground="#475467", relief="flat")
        estilo.map("Treeview", background=[("selected", tema.AZUL_SUAVE)],
                   foreground=[("selected", tema.TEXTO)])
        estilo.configure("Desarrollador.TCombobox", padding=4)

    # ------------------------------------------------------------------ barra superior
    def _crear_barra_superior(self):
        barra = tk.Frame(self, bg=tema.AZUL_OSCURO, height=66)
        barra.pack(side="top", fill="x")
        barra.pack_propagate(False)
        tk.Frame(self, bg=tema.CIAN, height=3).pack(side="top", fill="x")

        marca = tk.Frame(barra, bg=tema.AZUL_OSCURO)
        marca.pack(side="left", padx=22)
        tk.Label(marca, text="DL", bg=tema.BLANCO, fg=tema.AZUL_OSCURO, width=3,
                 font=(self.f["titulo"][0], 12, "bold"), pady=6).pack(side="left", padx=(0, 12))
        textos = tk.Frame(marca, bg=tema.AZUL_OSCURO)
        textos.pack(side="left")
        tk.Label(textos, text="DartLens", bg=tema.AZUL_OSCURO, fg=tema.BLANCO,
                 font=self.f["titulo"]).pack(anchor="w")
        tk.Label(textos, text="ANALIZADOR DE CÓDIGO DART", bg=tema.AZUL_OSCURO, fg="#cce9f8",
                 font=self.f["subtitulo"]).pack(anchor="w")

        controles = tk.Frame(barra, bg=tema.AZUL_OSCURO)
        controles.pack(side="right", padx=22)
        tk.Label(controles, text="Desarrollador", bg=tema.AZUL_OSCURO, fg="#dceef8",
                 font=self.f["pequena"]).pack(side="left", padx=(0, 8))
        selector = ttk.Combobox(controles, textvariable=self.desarrollador, state="readonly",
                                values=list(tema.DESARROLLADORES), width=16,
                                style="Desarrollador.TCombobox", font=self.f["normal"])
        selector.pack(side="left", padx=(0, 12))
        self.boton_cargar = tk.Button(controles, text="Cargar algoritmo de prueba (.dart)",
                                      command=self.cargar_algoritmo, bg=tema.BLANCO,
                                      fg=tema.AZUL_OSCURO, font=self.f["negrita"], relief="flat",
                                      padx=12, pady=6, cursor="hand2",
                                      activebackground="#f7fbfe")
        self.boton_cargar.pack(side="left")

    # ------------------------------------------------------------------ área de trabajo
    def _crear_area_trabajo(self):
        area = tk.Frame(self, bg=tema.FONDO)
        area.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        area.columnconfigure(0, weight=1, uniform="col")
        area.columnconfigure(1, weight=1, uniform="col")
        area.rowconfigure(0, weight=1)

        izquierda = tk.Frame(area, bg=tema.FONDO)
        izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        derecha = tk.Frame(area, bg=tema.FONDO)
        derecha.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        self.zona_editor = self._panel(izquierda)
        self.zona_editor.pack(side="top", fill="both", expand=True)
        self.zona_controles = self._panel(izquierda)
        self.zona_controles.pack(side="top", fill="x", pady=(9, 0))
        self.zona_resultados = self._panel(derecha)
        self.zona_resultados.pack(fill="both", expand=True)

    def _panel(self, padre):
        return tk.Frame(padre, bg=tema.BLANCO, highlightbackground=tema.LINEA,
                        highlightthickness=1)

    def _pendiente(self, zona, texto):
        tk.Label(zona, text=texto, bg=tema.BLANCO, fg=tema.TEXTO_SUAVE,
                 font=self.f["normal"], pady=40).pack(fill="both", expand=True)

    # ------------------------------------------------------------------ barra de estado
    def _crear_barra_estado(self):
        barra = tk.Frame(self, bg=tema.BLANCO, height=32, highlightbackground=tema.LINEA,
                         highlightthickness=1)
        barra.pack(side="bottom", fill="x", before=self.winfo_children()[0])
        barra.pack_propagate(False)

        self.punto_estado = tk.Label(barra, text="●", bg=tema.BLANCO, fg=tema.DESHABILITADO,
                                     font=self.f["normal"])
        self.punto_estado.pack(side="left", padx=(12, 4))
        self.texto_estado = tk.Label(barra, text="Listo", bg=tema.BLANCO, fg=tema.TEXTO,
                                     font=self.f["negrita"], anchor="w")
        self.texto_estado.pack(side="left", fill="x", expand=True)

        tk.Label(barra, textvariable=self.ultimo_log, bg=tema.BLANCO, fg="#475467",
                 font=self.f["codigo_peq"]).pack(side="right", padx=(0, 12))
        tk.Label(barra, text="Último log:", bg=tema.BLANCO, fg="#7b8794",
                 font=self.f["pequena"]).pack(side="right", padx=(0, 4))

        self.contadores = {}
        for fase in reversed(FASES):
            valor = tk.Label(barra, text="0", width=3, bg="#eef1f3", fg=tema.TEXTO_SUAVE,
                             font=self.f["negrita"])
            valor.pack(side="right", padx=(2, 14))
            tk.Label(barra, text=NOMBRE_FASE[fase] + "s", bg=tema.BLANCO, fg="#475467",
                     font=self.f["pequena"]).pack(side="right")
            self.contadores[fase] = valor

    # ------------------------------------------------------------------ componentes
    def _crear_componentes(self):
        # Editor de código (Juan Ayala)
        self._pendiente(self.zona_editor, "Editor de código: pendiente")
        # Fases de análisis (Juan Ayala)
        self._pendiente(self.zona_controles, "Fases de análisis: pendiente")
        # Resultados (Marcia Torres)
        self._pendiente(self.zona_resultados, "Resultados: pendiente")

    # ------------------------------------------------------------------ acciones comunes
    def usuario(self):
        return tema.DESARROLLADORES[self.desarrollador.get()]

    def _al_cambiar_desarrollador(self):
        if self.resultados:
            self.resultados.mostrar(self.sesion)

    def codigo(self):
        return self.editor.obtener_codigo() if self.editor else ""

    def cargar_algoritmo(self):
        if self.editor:
            self.editor.cargar_archivo()

    def mostrar_resultado(self, resultado):
        """Guarda el resultado de una fase y actualiza la barra de estado y los resultados."""
        self.sesion[resultado["fase"]] = resultado
        self.actualizar_estado()
        if self.resultados:
            self.resultados.mostrar(self.sesion)

    def limpiar_sesion(self):
        self.sesion.clear()
        self.actualizar_estado()
        if self.resultados:
            self.resultados.limpiar()
        if self.controles:
            self.controles.reiniciar()

    def codigo_modificado(self):
        """Si el código cambia, los resultados anteriores ya no valen."""
        if self.sesion:
            self.limpiar_sesion()

    def ir_a_linea(self, linea):
        if self.editor and linea:
            self.editor.resaltar_linea(linea)

    def registrar_log(self, nombre):
        self.ultimo_log.set(nombre)

    def actualizar_estado(self):
        for fase in FASES:
            n = len(self.sesion[fase]["errores"]) if fase in self.sesion else 0
            self.contadores[fase].configure(text=str(n), bg=tema.ERROR if n else "#eef1f3",
                                            fg=tema.BLANCO if n else tema.TEXTO_SUAVE)
        if not self.sesion:
            texto, color = "Listo", tema.DESHABILITADO
        else:
            ultima = [f for f in FASES if f in self.sesion][-1]
            errores = self.sesion[ultima]["errores"]
            if errores:
                color = tema.ERROR
                if len(errores) == 1:
                    linea, cat, msg = errores[0]
                    texto = f"Error {cat.split(' ')[0].lower()} en línea {linea}: {msg}"
                else:
                    texto = f"Análisis {NOMBRE_FASE[ultima].lower()}: {len(errores)} errores"
            else:
                color = tema.EXITO
                hechas = len(self.sesion)
                texto = ("Caso válido: las 3 fases se completaron sin errores" if hechas == 3
                         else f"{hechas} de 3 fases completadas: 0 errores")
        self.punto_estado.configure(fg=color)
        self.texto_estado.configure(text=texto, fg=color if self.sesion else tema.TEXTO)
# Fin aporte Mathias Giler
