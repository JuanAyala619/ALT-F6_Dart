# Inicio aporte Juan Ayala (JuanAyala619): editor de código Dart
# Editor con números de línea, carga de archivos .dart y resaltado de la línea de un error.
import os
import tkinter as tk
from tkinter import filedialog, messagebox

from interfaz import tema
from interfaz.analizador import RAIZ


class Editor(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=tema.BLANCO)
        self.app = app
        self._crear_encabezado()
        self._crear_area_codigo()

    def _crear_encabezado(self):
        f = self.app.f
        encabezado = tk.Frame(self, bg="#fafcfd", height=38, highlightbackground=tema.LINEA,
                              highlightthickness=1)
        encabezado.pack(side="top", fill="x")
        encabezado.pack_propagate(False)
        tk.Label(encabezado, text="</>", bg="#fafcfd", fg=tema.AZUL,
                 font=f["codigo_peq"]).pack(side="left", padx=(12, 6))
        tk.Label(encabezado, text="Editor Dart", bg="#fafcfd", fg=tema.TEXTO,
                 font=f["negrita"]).pack(side="left")
        tk.Frame(encabezado, bg=tema.LINEA, width=1).pack(side="left", fill="y", padx=8, pady=10)
        self.etiqueta_archivo = tk.Label(encabezado, text=self.app.archivo_actual, bg="#fafcfd",
                                         fg=tema.TEXTO_SUAVE, font=f["codigo_peq"])
        self.etiqueta_archivo.pack(side="left")
        tk.Label(encabezado, text="Dart", bg=tema.AZUL_SUAVE, fg=tema.AZUL_OSCURO,
                 font=(f["pequena"][0], 8, "bold"), padx=7, pady=2).pack(side="right", padx=12)

    def _crear_area_codigo(self):
        f = self.app.f
        cuerpo = tk.Frame(self, bg=tema.BLANCO)
        cuerpo.pack(side="top", fill="both", expand=True)

        self.numeros = tk.Text(cuerpo, width=4, padx=6, pady=10, takefocus=0, bd=0,
                               bg=tema.FONDO, fg="#98a2b3", font=f["codigo"], state="disabled",
                               cursor="arrow", highlightthickness=0)
        self.numeros.pack(side="left", fill="y")
        self.numeros.tag_configure("derecha", justify="right")
        self.numeros.tag_configure("error", background="#ffdede", foreground=tema.ERROR)

        barra_v = tk.Scrollbar(cuerpo, orient="vertical", command=self._desplazar)
        barra_v.pack(side="right", fill="y")
        barra_h = tk.Scrollbar(self, orient="horizontal")
        barra_h.pack(side="bottom", fill="x")

        self.texto = tk.Text(cuerpo, wrap="none", undo=True, bd=0, padx=12, pady=10,
                             bg="#fcfdfe", fg="#24364a", insertbackground=tema.AZUL,
                             font=f["codigo"], highlightthickness=0,
                             yscrollcommand=lambda *a: self._sincronizar(barra_v, *a),
                             xscrollcommand=barra_h.set)
        self.texto.pack(side="left", fill="both", expand=True)
        barra_h.configure(command=self.texto.xview)
        self.texto.tag_configure("error", background=tema.ERROR_SUAVE)

        self.texto.bind("<<Modified>>", self._al_modificar)
        self.texto.bind("<Tab>", self._tabulador)
        self.numeros.bind("<MouseWheel>", lambda e: self.texto.event_generate("<MouseWheel>", delta=e.delta))
        self._actualizar_numeros()

    # ------------------------------------------------------------------ desplazamiento
    def _desplazar(self, *args):
        self.texto.yview(*args)
        self.numeros.yview(*args)

    def _sincronizar(self, barra, primero, ultimo):
        barra.set(primero, ultimo)
        self.numeros.yview_moveto(primero)

    def _tabulador(self, _evento):
        self.texto.insert("insert", "  ")
        return "break"

    # ------------------------------------------------------------------ números de línea
    def _actualizar_numeros(self):
        total = int(self.texto.index("end-1c").split(".")[0])
        self.numeros.configure(state="normal")
        self.numeros.delete("1.0", "end")
        self.numeros.insert("1.0", "\n".join(str(i) for i in range(1, total + 1)), "derecha")
        self.numeros.configure(state="disabled")
        self.numeros.yview_moveto(self.texto.yview()[0])

    def _al_modificar(self, _evento=None):
        if self.texto.edit_modified():
            self.texto.edit_modified(False)
            self._actualizar_numeros()
            self.quitar_resaltado()
            self.app.codigo_modificado()

    # ------------------------------------------------------------------ operaciones
    def obtener_codigo(self):
        return self.texto.get("1.0", "end-1c")

    def poner_codigo(self, codigo, nombre_archivo=None):
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", codigo)
        self.texto.edit_reset()
        if nombre_archivo:
            self.app.archivo_actual = nombre_archivo
            self.etiqueta_archivo.configure(text=nombre_archivo)
        self._al_modificar()

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Cargar algoritmo de prueba",
            initialdir=os.path.join(RAIZ, "algoritmos"),
            filetypes=[("Código Dart", "*.dart"), ("Todos los archivos", "*.*")])
        if not ruta:
            return
        try:
            with open(ruta, encoding="utf-8") as archivo:
                self.poner_codigo(archivo.read(), os.path.basename(ruta))
        except (OSError, UnicodeDecodeError) as error:
            messagebox.showerror("No se pudo abrir el archivo", str(error))

    def limpiar(self):
        self.poner_codigo("", "algoritmo.dart")

    def resaltar_linea(self, linea):
        """Marca en rojo la línea de un error y la lleva a la vista."""
        self.quitar_resaltado()
        self.texto.tag_add("error", f"{linea}.0", f"{linea}.0 lineend +1c")
        self.numeros.tag_add("error", f"{linea}.0", f"{linea}.0 lineend")
        self.texto.see(f"{linea}.0")
        self.texto.mark_set("insert", f"{linea}.0")
        self.texto.focus_set()

    def quitar_resaltado(self):
        self.texto.tag_remove("error", "1.0", "end")
        self.numeros.tag_remove("error", "1.0", "end")
# Fin aporte Juan Ayala
