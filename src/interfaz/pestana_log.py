# Inicio aporte Marcia Torres (marciatorresg): pestaña Log y diálogo para guardar
# Muestra el registro de las fases ejecutadas y guarda un log por fase en logs/ con el
# formato pedido: lexico-usuarioGit-fecha-hora.txt, sintactico-... y semantico-...
import tkinter as tk
from datetime import datetime

from interfaz import tema
from interfaz.analizador import FASES, NOMBRE_FASE, texto_log, nombre_log, guardar_log


class PestanaLog(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=tema.BLANCO)
        self.app = app
        self.sesion = {}
        f = app.f
        barra = tk.Frame(self, bg=tema.BLANCO, padx=12, pady=9, highlightbackground=tema.LINEA,
                         highlightthickness=1)
        barra.pack(fill="x")
        textos = tk.Frame(barra, bg=tema.BLANCO)
        textos.pack(side="left")
        tk.Label(textos, text="Registro del análisis", bg=tema.BLANCO, fg=tema.TEXTO,
                 font=f["negrita"]).pack(anchor="w")
        tk.Label(textos, text="Sesión actual", bg=tema.BLANCO, fg=tema.TEXTO_SUAVE,
                 font=f["pequena"]).pack(anchor="w")
        self.boton_guardar = tk.Button(barra, text="Guardar log", command=self.abrir_dialogo,
                                       bg=tema.AZUL, fg=tema.BLANCO, activebackground=tema.AZUL_OSCURO,
                                       activeforeground=tema.BLANCO, font=f["negrita"],
                                       relief="flat", padx=13, pady=6, cursor="hand2")
        self.boton_guardar.pack(side="right")

        self.texto = tk.Text(self, bd=0, padx=14, pady=12, bg="#f8fafb", fg="#36485c",
                             font=f["codigo_peq"], wrap="none", highlightthickness=0)
        self.texto.pack(fill="both", expand=True)
        self.dialogo = None
        self.mostrar({})

    def mostrar(self, sesion):
        self.sesion = dict(sesion)
        usuario = self.app.usuario()
        lineas = ["[DartLens] Inicio de sesión",
                  f"Desarrollador: {self.app.desarrollador.get()} ({usuario})",
                  f"Archivo: {self.app.archivo_actual}",
                  "-" * 48]
        if not sesion:
            lineas.append("Esperando análisis...")
        for fase in FASES:
            if fase in sesion:
                lineas.append("")
                lineas.append(f"===== Análisis {NOMBRE_FASE[fase].lower()} =====")
                lineas.append(texto_log(sesion[fase], self.app.archivo_actual, usuario).rstrip())
        self.texto.configure(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", "\n".join(lineas))
        self.texto.configure(state="disabled")
        self.boton_guardar.configure(state="normal" if sesion else "disabled",
                                     bg=tema.AZUL if sesion else "#eef1f3")

    def abrir_dialogo(self):
        if self.sesion:
            self.dialogo = DialogoGuardarLog(self.app, self.sesion)


class DialogoGuardarLog(tk.Toplevel):
    """Confirma los nombres de los logs (uno por fase ejecutada) y los guarda en logs/."""

    def __init__(self, app, sesion):
        super().__init__(app)
        self.app = app
        self.sesion = sesion
        usuario = app.usuario()
        momento = datetime.now()
        self.archivos = [(fase, nombre_log(fase, usuario, momento)) for fase in FASES if fase in sesion]
        f = app.f

        self.title("Guardar log de análisis")
        self.configure(bg=tema.BLANCO)
        self.resizable(False, False)
        self.transient(app)

        cabecera = tk.Frame(self, bg=tema.BLANCO, padx=18, pady=14)
        cabecera.pack(fill="x")
        self.titulo = tk.Label(cabecera, text="Guardar log de análisis", bg=tema.BLANCO,
                               fg="#25364a", font=(f["negrita"][0], 12, "bold"))
        self.titulo.pack(anchor="w")
        self.subtitulo = tk.Label(cabecera, text="Confirma el nombre de los archivos antes de guardarlos.",
                                  bg=tema.BLANCO, fg=tema.TEXTO_SUAVE, font=f["pequena"])
        self.subtitulo.pack(anchor="w")
        tk.Frame(self, bg=tema.LINEA, height=1).pack(fill="x")

        cuerpo = tk.Frame(self, bg=tema.BLANCO, padx=18, pady=14)
        cuerpo.pack(fill="x")
        tk.Label(cuerpo, text="Archivos (carpeta logs/)", bg=tema.BLANCO, fg="#344054",
                 font=f["negrita"]).pack(anchor="w", pady=(0, 6))
        self.etiquetas = []
        for _, nombre in self.archivos:
            fila = tk.Label(cuerpo, text="📄  " + nombre, bg=tema.BLANCO, fg="#344054", anchor="w",
                            font=f["codigo_peq"], padx=10, pady=8, highlightthickness=1,
                            highlightbackground="#aebbc5")
            fila.pack(fill="x", pady=2)
            self.etiquetas.append(fila)
        self.nota = tk.Label(cuerpo, text="Se guardará un archivo de texto (.txt) por cada fase ejecutada.",
                             bg="#f0f9fe", fg="#476372", font=f["pequena"], anchor="w", padx=9, pady=7)
        self.nota.pack(fill="x", pady=(10, 0))

        pie = tk.Frame(self, bg="#fafbfc", padx=18, pady=11)
        pie.pack(fill="x")
        self.boton_guardar = tk.Button(pie, text="Guardar", command=self.guardar, bg=tema.AZUL,
                                       fg=tema.BLANCO, activebackground=tema.AZUL_OSCURO,
                                       activeforeground=tema.BLANCO, font=f["negrita"], relief="flat",
                                       padx=14, pady=6, cursor="hand2")
        self.boton_guardar.pack(side="right")
        self.boton_cancelar = tk.Button(pie, text="Cancelar", command=self.destroy, bg=tema.BLANCO,
                                        fg="#344054", font=f["negrita"], relief="flat", padx=14,
                                        pady=6, cursor="hand2")
        self.boton_cancelar.pack(side="right", padx=8)

        self.update_idletasks()
        x = app.winfo_rootx() + (app.winfo_width() - self.winfo_width()) // 2
        y = app.winfo_rooty() + (app.winfo_height() - self.winfo_height()) // 3
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        self.grab_set()

    def guardar(self):
        usuario = self.app.usuario()
        for fase, nombre in self.archivos:
            guardar_log(nombre, texto_log(self.sesion[fase], self.app.archivo_actual, usuario))
        self.app.registrar_log(self.archivos[-1][1])
        self.titulo.configure(text="Log guardado correctamente")
        self.subtitulo.configure(text="Los archivos están en la carpeta logs del repositorio.")
        for fila in self.etiquetas:
            fila.configure(fg=tema.EXITO, highlightbackground="#9bc59d", bg="#fbfefb")
        self.nota.pack_forget()
        self.boton_cancelar.pack_forget()
        self.boton_guardar.configure(text="Cerrar", command=self.destroy)
# Fin aporte Marcia Torres
