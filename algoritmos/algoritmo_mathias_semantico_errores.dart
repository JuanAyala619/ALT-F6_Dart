// Reglas: conversión de double a int y retorno en funciones void
double precio = 7.5;
int entero = precio;
int mitad = 9 / 2;
const int maximo = 3.5;
int bien = precio.toInt();
int division = 9 ~/ 2;

void saludar(String nombre) {
  print("Hola $nombre");
  return 5;
}

void terminar() {
  return;
}

int doble(int n) {
  return n * 2;
}