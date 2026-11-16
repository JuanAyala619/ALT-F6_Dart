// algoritmo_juan_semantico_errores.dart - Juan Ayala
// Reglas: inmutabilidad de const/final y condiciones booleanas en if/while
const int maximo = 10;
final double tasa = 0.5;
int contador = 0;

maximo = 20;
tasa = 0.8;
contador++;

while (contador) {
    contador++;
}

if (contador + 1) {
    print(contador);
}

while (contador < maximo) {
    contador++;
}