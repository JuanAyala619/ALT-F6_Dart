// Reglas: conversión de double a int y retorno en funciones void
double ancho = 4.0;
double altura = 2.5;
double area = ancho * altura;

int areaEntera = area;
int areaBien = area.toInt();
int promedio = (10 + 5) / 2;
int mitad = 15 ~/ 2;

void imprimirArea(double valor) {
  print("Área: $valor");
  return valor;
}

void main() {
  imprimirArea(area);
}