// Constantes en tiempo de compilación
const int limite = 5;
const pi = 3.14;

/* Función sin retorno
   que saluda a una persona */
void saludar(String nombre) {
  print("Hola $nombre");
}

void main() {
  saludar("Mathias");

  // Tupla (record) con edad y nombre
  (int, String) persona = (20, "Ana");
  print(persona);

  // Bucle for
  for (int i = 0; i < limite; i++) {
    print("Vuelta ${i + 1}");
  }

  // Conversión explícita de double a int
  double area = pi * 2.0 * 2.0;
  int areaEntera = area.toInt();
  print("Área aproximada: $areaEntera");

  String? apellido = null;
  apellido ??= "Giler";
  print(apellido);

  // División entera y residuo
  int mitad = limite ~/ 2;
  int sobra = limite % 2;
  print("Mitad: $mitad, sobra: $sobra");
}