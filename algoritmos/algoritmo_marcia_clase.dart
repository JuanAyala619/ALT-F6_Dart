// Algoritmo con clase - Marcia Torres (marciatorresg)
// Cubre: clase con propiedades, constructor y metodos, objeto, var, late, ??=, if/else if/else, Set

class Persona {
  String nombre;
  int edad;

  Persona(this.nombre, this.edad);

  String descripcion() {
    return this.nombre;
  }

  bool esMayor() {
    return this.edad >= 18 && this.edad != 0;
  }

  int doble(int n) => n * 2;

  void mostrar() {
    print(this.edad);
  }
}

int limite(int a, int b) {
  if (a > b) {
    return a;
  } else if (a == b) {
    return 0;
  } else {
    return b;
  }
}

void main() {
  Persona ana = Persona("Ana", 20);
  var mensaje = ana.descripcion();
  late int total;
  total = limite(3, 9);
  Set<int> numeros = {1, 2, 3};
  numeros.add(total);
  String? extra;
  extra ??= "pendiente";

  if (ana.esMayor() && !(total < 0) || total == 9) {
    ana.mostrar();
  } else {
    print(mensaje);
  }
}