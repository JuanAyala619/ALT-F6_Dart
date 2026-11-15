// Algoritmo de prueba sintáctico - Juan Ayala
//Cubre: tipado explícito, aritméticas, listas, while y lambda
int duplicar(int n) => n * 2;
int sumar(int a, int b) => a + b;
int negativo = -4;

List<int> numeros = [1, 2, 3, 4];
List<int> vacia = [];
int indice = 0;
int suma = 0;
double promedio = 2.5;
bool activo = true;

int total = (suma + 3) * 2 - 1;
int entera = total ~/ 2;
int residuo = total % 3;
int primero = numeros[0];
int doble = duplicar(suma);

while (activo) {
  suma = suma + numeros[indice];
  indice++;
}