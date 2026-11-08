// Algoritmo de prueba - Marcia Torres (marciatorresg)
// Cubre: var, if/else, conjuntos, funcion con retorno, cadenas, relacionales, logicos y asignacion

/// Retorna el mayor de dos enteros
int mayor(int a, int b) {
  if (a >= b) {
    return a;
  } else {
    return b;
  }
}

bool esValido(int edad, bool activo) {
  return edad >= 18 && activo || edad == 65;
}

void main() {
  var nombre = 'Marcia';
  var apellido = "Torres";
  var saludo = 'Hola $nombre, bienvenida';
  var calculo = "El mayor es ${mayor(3, 7)}";
  var ruta = r'C:\datos\nuevo$x';
  var texto = '''Linea uno
Linea dos''';
  var doc = """Otra cadena
de varias lineas""";

  Set<int> conjunto = {1, 2, 3, 3};
  Set<String> nombres = {'ana', "luis"};
  conjunto.add(4);

  int x = mayor(10, 20);
  String? opcional;
  opcional ??= 'valor por defecto';

  if (x > 5 && x != 15) {
    print(saludo);
  } else if (x <= 5 || !esValido(x, true)) {
    print(calculo);
  } else {
    print(conjunto);
  }

  if (x < 100) {
    print(x);
  }

  /* comentario
     de bloque */
  final bool igual = (x == 20);
  late int tardio;
  tardio = x;
  var nada = null;
  var si = true; # @
}
