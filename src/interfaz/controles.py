# Inicio aporte Juan Ayala (JuanAyala619): panel de fases de análisis
# Las fases se ejecutan en orden: la siguiente se habilita solo cuando la anterior
# termina sin errores, igual que en el prototipo de Figma.
import tkinter as tk

from interfaz import tema
from interfaz.analizador import FASES, NOMBRE_FASE, ANALIZAR


class PanelFases(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=tema.BLANCO, padx=12, pady=10)
        self.app = app
        self.completadas = 0      # cuántas fases seguidas pasaron sin errores
        f = app.f

        encabezado = tk.Frame(self, bg=tema.BLANCO)
        encabezado.pack(fill="x", pady=(0, 9))
        tk.Label(encabezado, text="Fases de análisis", bg=tema.BLANCO, fg=tema.TEXTO,
                 font=f["negrita"]).pack(side="left")
        tk.Label(encabezado, text="Ejecuta las fases en orden", bg=tema.BLANCO,
                 fg=tema.TEXTO_SUAVE, font=f["pequena"]).pack(side="left", padx=8)
        tk.Label(encabezado, text="1 Léxico → 2 Sintáctico → 3 Semántico", bg="#f1f4f6",
                 fg=tema.TEXTO_SUAVE, font=f["codigo_peq"], padx=7, pady=2).pack(side="right")

        fila = tk.Frame(self, bg=tema.BLANCO)
        fila.pack(fill="x")
        self.botones = {}
        for i, fase in enumerate(FASES):
            boton = tk.Button(fila, text=f"▶  Analizar {NOMBRE_FASE[fase].lower()}",
                              command=lambda fs=fase: self.ejecutar(fs), font=f["negrita"],
                              relief="flat", bd=1, pady=7, cursor="hand2",
                              highlightthickness=1)
            boton.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 7, 0))
            fila.columnconfigure(i, weight=1)
            self.botones[fase] = boton

        self.ayuda = tk.Label(self, text="", bg=tema.BLANCO, fg=tema.TEXTO_SUAVE,
                              font=f["pequena"], anchor="w")
        self.ayuda.pack(fill="x", pady=(6, 0))

        acciones = tk.Frame(self, bg=tema.BLANCO)
        acciones.pack(fill="x", pady=(6, 0))
        tk.Button(acciones, text="▶  Ejecutar las 3 fases", command=self.ejecutar_todas,
                  bg=tema.EXITO, fg=tema.BLANCO, activebackground="#246728",
                  activeforeground=tema.BLANCO, font=f["negrita"], relief="flat", padx=13,
                  pady=6, cursor="hand2").pack(side="left")
        tk.Button(acciones, text="Limpiar", command=self.limpiar, bg=tema.BLANCO,
                  fg=tema.TEXTO_SUAVE, font=f["negrita"], relief="flat", padx=13, pady=6,
                  cursor="hand2", activebackground=tema.FONDO).pack(side="left", padx=8)
        self.reiniciar()

    # ------------------------------------------------------------------ estado de botones
    def _refrescar(self):
        for i, fase in enumerate(FASES):
            boton = self.botones[fase]
            if i > self.completadas:
                boton.configure(state="disabled", bg="#eef1f3", fg=tema.DESHABILITADO,
                                disabledforeground=tema.DESHABILITADO, cursor="arrow")
            elif i == self.completadas:
                boton.configure(state="normal", bg=tema.AZUL, fg=tema.BLANCO,
                                activebackground=tema.AZUL_OSCURO, activeforeground=tema.BLANCO,
                                cursor="hand2")
            else:
                boton.configure(state="normal", bg=tema.BLANCO, fg="#344054",
                                activebackground="#f7fbfe", activeforeground=tema.AZUL_OSCURO,
                                cursor="hand2")
        if self.completadas < len(FASES) and self.completadas > 0:
            self.ayuda.configure(text=f"Siguiente: análisis {NOMBRE_FASE[FASES[self.completadas]].lower()}.")
        elif self.completadas == 0:
            self.ayuda.configure(text="Escribe o carga código Dart y empieza por el análisis léxico.")
        else:
            self.ayuda.configure(text="Las 3 fases terminaron sin errores.")

    def reiniciar(self):
        self.completadas = 0
        self._refrescar()

    # ------------------------------------------------------------------ ejecución
    def ejecutar(self, fase):
        indice = FASES.index(fase)
        if indice > self.completadas:
            return
        codigo = self.app.codigo()
        if not codigo.strip():
            self.ayuda.configure(text="No hay código para analizar.", fg=tema.ERROR)
            return
        self.ayuda.configure(fg=tema.TEXTO_SUAVE)
        # Al repetir una fase, los resultados de las fases siguientes dejan de valer
        for siguiente in FASES[indice:]:
            self.app.sesion.pop(siguiente, None)
        resultado = ANALIZAR[fase](codigo)
        self.app.mostrar_resultado(resultado)
        if resultado["errores"]:
            self.completadas = indice
            self._refrescar()
            siguiente = ("vuelve a analizar." if fase == FASES[-1]
                         else "habilita la siguiente fase.")
            self.ayuda.configure(text=f"Corrige los errores {NOMBRE_FASE[fase].lower()}s y "
                                      f"{siguiente}", fg=tema.ERROR)
            return False
        self.completadas = indice + 1
        self._refrescar()
        return True

    def ejecutar_todas(self):
        """Ejecuta las fases en orden y se detiene en la primera que tenga errores."""
        self.completadas = 0
        for fase in FASES:
            if not self.ejecutar(fase):
                break

    def limpiar(self):
        if self.app.editor:
            self.app.editor.limpiar()
        self.app.limpiar_sesion()
# Fin aporte Juan Ayala
