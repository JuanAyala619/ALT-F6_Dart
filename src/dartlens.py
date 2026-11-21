# Inicio aporte Mathias Giler (matheoglg): punto de entrada de la interfaz gráfica
# Uso, desde la raíz del repositorio:  python src/dartlens.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interfaz.app import DartLens

if __name__ == "__main__":
    DartLens().mainloop()
# Fin aporte Mathias Giler
