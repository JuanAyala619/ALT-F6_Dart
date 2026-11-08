int duplicar(int n) => n * 2;

void main() {
  List<int> numeros = [1, 2, 3, 4];
  int indice = 0;
  int suma = 0;
  double promedio = 2.5;
  double grande = 1e5;

  while (indice < 4) {
    suma = suma + numeros[indice];
    indice++;
  }

  int resta = suma - 2;
  int producto = suma * 3;
  double mitad = suma / 2;
  int entera = suma ~/ 2;
  int residuo = suma % 3;
  indice--;

  print(duplicar(suma));
  print("Suma: $suma");
  print(promedio);
}