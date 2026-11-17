// algoritmo_juan_semantico_errores.dart - Juan Ayala
// Reglas: inmutabilidad de const/final y condiciones booleanas en if/while
const int maximo = 10;
final double tasa = 0.5;
int contador = 0;
final String saludo = "Hola";
const String bienvenida = "Bienvenidos";
final bool verdadero = true;

maximo = 20;
tasa = 0.8;
contador++;
saludo = "Adios";
bienvenida = "Hasta la próxima";

while (saludo) {
    contador++;
    saludo ="Quiza nos veamos";
}

if (contador + 1) {
    print(contador);
}

while (contador < maximo) {
    contador++;
}

if (maximo == 10){
    verdadero = false;
}