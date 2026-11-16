import ply.yacc as yacc
from lexer_dart import tokens

errores_sintacticos = []
start = 'programa'
#Inicio aporte Juan Ayala: base analizador semántico
tabla_simbolos = {}
tabla_funciones = {}
pila_funciones = []
errores_semanticos = []
def reiniciar_semantico():
    tabla_simbolos.clear()
    tabla_funciones.clear()
    pila_funciones.clear()
    errores_semanticos.clear()

def error_semantico(linea, categoria, mensaje):
    errores_semanticos.append((linea, categoria, mensaje))

def declarar(nombre, tipo, mutable=True):
    tabla_simbolos[nombre] = {'tipo': tipo, 'mutable': mutable}

def tipo_base(tipo):
    if isinstance(tipo, str):
        while len(tipo) > 0 and tipo[-1] == '?':
            tipo = tipo[:-1]
        return tipo
    else:
        return None
#fin aporte Juan Ayala
def p_programa(p):
    '''programa : declaraciones'''

def p_declaraciones(p):
    '''declaraciones : declaracion
                    | declaraciones declaracion'''

def p_tipo(p):
    '''tipo : INT
            | DOUBLE
            | STRING
            | BOOL'''
    p[0]=p[1]

def p_expresion(p):
    '''expresion : ENTERO
                | DECIMAL
                | CADENA
                | TRUE
                | FALSE'''
    tipos = {'ENTERO': 'int', 'DECIMAL': 'double', 'CADENA': 'String',
             'TRUE': 'bool', 'FALSE': 'bool'}
    p[0] = tipos[p.slice[1].type]

def p_expresion_id(p):
    '''expresion : ID'''
    simbolo = tabla_simbolos.get(p[1])
    if simbolo is not None:
        p[0] = simbolo['tipo']
    else:
        p[0] = None

def p_expresion_agrupada(p):
    '''expresion : PARENTESIS_IZQ expresion PARENTESIS_DER
                | operacion_aritmetica'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_cuerpo_base(p):
    '''cuerpo_base : LLAVE_IZQ declaraciones LLAVE_DER
                | LLAVE_IZQ LLAVE_DER'''
def p_error(p):
    if p:
        errores_sintacticos.append((p.lineno, f"token inesperado '{p.value}'"))
    else:
        errores_sintacticos.append((None, "fin de archivo inesperado"))

# Inicio aporte Juan Ayala (JuanAyala619): reglas de precedencia 
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUAL', 'DIFERENTE'),
    ('left', 'MENOR_QUE', 'MAYOR_QUE', 'MENOR_IGUAL', 'MAYOR_IGUAL'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION', 'DIV_ENTERA', 'MODULO'),
    ('right', 'UMENOS'),
    ('right', 'NOT'),
)
def p_expresion_menos_unario(p):
    '''expresion : RESTA expresion %prec UMENOS'''
    p[0] = p[2]
# fin aporte Juan Ayala
#Declaración de variables
    #Inicio aporte Juan Ayala: Tipado explícito
def p_declaracion_tipado_explicito(p):
    '''declaracion : tipado_explicito'''

def p_tipado_explicito(p):
    '''tipado_explicito : tipo ID ASIGNACION expresion PUNTO_COMA
                        | tipo ID PUNTO_COMA'''
    declarar(p[2], p[1])
    if len(p) == 6:
        # Regla semántica (Mathias Giler) - Conversión
        verificar_conversion(p[1], p[4], p[2], p.lineno(2))

    #fin aporte Juan Ayala
    #Inicio aporte Marcia Torres (marciatorresg): Tipado inferido
# Regla: declaración con tipado inferido
#   var [nombre] = [valor];
def p_declaracion_tipado_inferido(p):
    '''declaracion : tipado_inferido'''

def p_tipado_inferido(p):
    '''tipado_inferido : VAR ID ASIGNACION expresion PUNTO_COMA
                       | VAR ID PUNTO_COMA'''

# Regla: declaración con inicialización tardía
#   late [tipo] [nombre];
def p_declaracion_late(p):
    '''declaracion : LATE tipo ID PUNTO_COMA'''

# Regla: asignación si es null
#   [nombre] ??= [valor];
def p_asignacion_null(p):
    '''asignacion : ID ASIGNACION_NULL expresion PUNTO_COMA'''
    #fin aporte Marcia Torres

#Inicio aporte Mathias Giler (matheoglg): Constante en tiempo de compilación
def p_declaracion_constante(p):
    '''declaracion : constante'''

def p_constante(p):
    '''constante : CONST tipo ID ASIGNACION expresion PUNTO_COMA 
                | CONST ID ASIGNACION expresion PUNTO_COMA
                | FINAL tipo ID ASIGNACION expresion PUNTO_COMA
                | FINAL ID ASIGNACION expresion PUNTO_COMA'''
    if len(p) == 7:
        declarar(p[3], p[2], mutable=False)
        verificar_conversion(p[2], p[5], p[3], p.lineno(3))
    else:
        declarar(p[2], p[4], mutable=False)

def verificar_conversion(tipo_destino, tipo_valor, nombre, linea):
    if tipo_base(tipo_destino) == 'int' and tipo_base(tipo_valor) == 'double':
        error_semantico(linea, 'Conversión',
                        f"no se puede asignar un double a '{nombre}' de tipo int "
                        f"sin conversión explícita. Usa .toInt() o ~/")
        
    #fin aporte Mathias Giler

#Inicio aporte Juan Ayala: Expresiones aritméticas
#Regla semántica: una variable declarada con const o final no se puede volver a asignar
def verificar_mutable(nombre, linea):
    simbolo = tabla_simbolos.get(nombre)
    if simbolo and not simbolo['mutable']:
        error_semantico(linea, 'Asignación de tipo',
                        f"'{nombre}' es const o final y no se puede modificar")

def p_declaracion_asignacion(p):
    '''declaracion : asignacion'''

def p_asignacion(p):
    '''asignacion : ID ASIGNACION expresion PUNTO_COMA'''
    verificar_mutable(p[1],p.lineno(1))

def p_operacion_aritmeticas(p):
    '''operacion_aritmetica : expresion SUMA expresion
                            | expresion RESTA expresion
                            | expresion MULTIPLICACION expresion
                            | expresion DIVISION expresion
                            | expresion DIV_ENTERA expresion
                            | expresion MODULO expresion'''

def p_declaracion_incremento_o_decremento(p):
    '''declaracion : incremento_o_decremento'''

def p_incremento_o_decremento(p):
    '''incremento_o_decremento : ID INCREMENTO PUNTO_COMA
                                | ID DECREMENTO PUNTO_COMA'''
    verificar_mutable(p[1], p.lineno(1))
#fin aporte Juan Ayala

#Inicio aporte Marcia Torres: Expresiones booleanas
# Regla: expresiones booleanas con operadores relacionales y de igualdad
#   [valor_1] (< > <= >= == !=) [valor_2]
def p_expresion_relacional(p):
    '''expresion : expresion MENOR_QUE expresion
                 | expresion MAYOR_QUE expresion
                 | expresion MENOR_IGUAL expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion IGUAL expresion
                 | expresion DIFERENTE expresion'''

# Regla: conectores lógicos (uno o más)
#   [condición_1] && [condición_2] || [condición_3]
def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''

# Regla: negación
#   ![condición]
def p_expresion_not(p):
    '''expresion : NOT expresion'''
#fin aporte Marcia Torres

#Estructuras de Control
    #Inicio aporte Juan Ayala: Bucle while
    #Regla semántica: la condición de un if o un while tiene que ser de tipo bool
def verificar_condicion(tipo, estructura, linea):
    tipo = tipo_base(tipo)
    if tipo is not None and tipo != 'bool':
        mensaje = "la condición del " + estructura + " debe ser bool, se encontró '" + tipo + "'"
        error_semantico(linea, 'Estructuras de control', mensaje)

def p_declaracion_bucle_while(p):
    '''declaracion : bucle_while'''

def p_bucle_while(p):
    '''bucle_while : WHILE PARENTESIS_IZQ expresion PARENTESIS_DER cuerpo_base'''
    verificar_condicion(p[3], 'while', p.lineno(1))
    #fin aporte Juan Ayala
    #Inicio aporte Marcia Torres: if-else
# Regla: if / else if / else
#   if ([condición]) { ... } else if ([condición]) { ... } else { ... }
def p_declaracion_condicional(p):
    '''declaracion : condicional_if'''

def p_condicional_if(p):
    '''condicional_if : IF PARENTESIS_IZQ expresion PARENTESIS_DER cuerpo_base
                      | IF PARENTESIS_IZQ expresion PARENTESIS_DER cuerpo_base ELSE cuerpo_base
                      | IF PARENTESIS_IZQ expresion PARENTESIS_DER cuerpo_base ELSE condicional_if'''
    #fin aporte Marcia Torres
    #Regla semántica (Juan Ayala)
    verificar_condicion(p[3], 'if', p.lineno(1))

    #Inicio aporte Mathias Giler: Bucle for
def p_declaracion_bucle_for(p):
    '''declaracion : bucle_for'''

def p_bucle_for(p):
    '''bucle_for : FOR PARENTESIS_IZQ for_control PARENTESIS_DER cuerpo_base'''

# Las tres partes del paréntesis, separadas por ';'
def p_for_control(p):
    '''for_control : for_inicio PUNTO_COMA expresion PUNTO_COMA for_actualizacion'''

def p_for_inicio(p):
    '''for_inicio : tipo ID ASIGNACION expresion
                  | VAR ID ASIGNACION expresion
                  | ID ASIGNACION expresion'''
    if len(p) == 5:
        declarar(p[2], p[4] if p[1] == 'var' else p[1])

def p_for_actualizacion(p):
    '''for_actualizacion : ID INCREMENTO
                         | ID DECREMENTO
                         | ID ASIGNACION expresion'''
    #fin aporte Mathias Giler
#Estructuras de datos
    #Inicio aporte Juan Ayala: Listas
def p_declaracion_lista(p):
    '''declaracion : lista'''
def p_lista(p):
    '''lista : previo_asignacion CORCHETE_IZQ elementos CORCHETE_DER PUNTO_COMA
                | previo_asignacion CORCHETE_IZQ CORCHETE_DER PUNTO_COMA'''

def p_previo_asignacion(p):
    '''previo_asignacion : LIST MENOR_QUE tipo MAYOR_QUE ID ASIGNACION'''
    declarar(p[5], f'List<{p[3]}>')

def p_elementos(p):
    '''elementos : expresion
                | elementos COMA expresion'''  

def p_expresion_acceso_lista(p):
    '''expresion : ID CORCHETE_IZQ expresion CORCHETE_DER'''      
    simbolo = tabla_simbolos.get(p[1])
    if simbolo is not None:
        tipo = simbolo['tipo']
    else:
        tipo = None
    if tipo is not None and tipo[0:5] == 'List<':
        p[0]= tipo[5:-1]
    else:
        p[0] = None

    #fin aporte Juan Ayala
    #Inicio aporte Marcia Torres: Conjuntos
# Regla: conjuntos
#   Set<[tipo]> [nombre] = {[valor_1], [valor_2], ...};
def p_declaracion_conjunto(p):
    '''declaracion : conjunto'''

def p_conjunto(p):
    '''conjunto : SET MENOR_QUE tipo MAYOR_QUE ID ASIGNACION LLAVE_IZQ elementos LLAVE_DER PUNTO_COMA
                | SET MENOR_QUE tipo MAYOR_QUE ID ASIGNACION LLAVE_IZQ LLAVE_DER PUNTO_COMA'''
    #fin aporte Marcia Torres
    
    #Inicio aporte Mathias Giler: Tuplas/Records

# Regla: tuplas / records
#   ([tipo_1], [tipo_2], ...) [nombre] = ([valor_1], [valor_2], ...);
def p_declaracion_record(p):
    '''declaracion : record'''

def p_record(p):
    '''record : tipo_record ID ASIGNACION expresion PUNTO_COMA'''
    declarar(p[2], 'Record')

def p_tipo_record(p):
    '''tipo_record : PARENTESIS_IZQ tipo COMA lista_tipos PARENTESIS_DER'''

def p_lista_tipos(p):
    '''lista_tipos : tipo
                   | lista_tipos COMA tipo'''

# Valor de una tupla: necesita al menos 2 elementos; con uno solo es una expresión entre paréntesis
def p_expresion_record(p):
    '''expresion : PARENTESIS_IZQ expresion COMA elementos PARENTESIS_DER'''
    p[0] = 'Record'
    #fin aporte Mathias Giler

#Declaraciones de funciones
    #Inicio aporte Juan Ayala: Lambda
def p_declaracion_lambda(p):
    '''declaracion : lambda'''

def p_lambda(p):
    '''lambda : tipado_comun FLECHA expresion PUNTO_COMA'''
    pila_funciones.pop()

def p_tipado_comun(p):
    '''tipado_comun : tipo ID PARENTESIS_IZQ parametros PARENTESIS_DER
                    | tipo ID PARENTESIS_IZQ PARENTESIS_DER'''
    tabla_funciones[p[2]] = p[1]
    pila_funciones.append(p[1])
    
def p_parametros(p):
    '''parametros : tipo ID 
                | parametros COMA tipo ID'''
    if len(p)==3:
        declarar(p[2], p[1])
    else:
        declarar(p[4], p[3])

def p_expresion_llamada_funcion(p):
    '''expresion : ID PARENTESIS_IZQ elementos PARENTESIS_DER
                 | ID PARENTESIS_IZQ PARENTESIS_DER'''
    p[0] = tabla_funciones.get(p[1])
    #fin aporte Juan Ayala
    #Inicio aporte Marcia Torres: Función con retorno
# Regla: función con retorno
#   [tipo] [nombre]([parámetros]) { ... return [valor]; }
# Reutiliza tipado_comun (tipo, nombre y parámetros) que definió Juan para la lambda
def p_declaracion_funcion_retorno(p):
    '''declaracion : funcion_retorno'''

def p_funcion_retorno(p):
    '''funcion_retorno : tipado_comun cuerpo_base'''

def p_declaracion_return(p):
    '''declaracion : RETURN expresion PUNTO_COMA
                   | RETURN PUNTO_COMA'''
    # Regla semántica (Mathias Giler) Retorno de funciones
    # una función de tipo void no puede devolver un valor
    if len(p) == 4 and pila_funciones and pila_funciones[-1] == 'void':
        error_semantico(p.lineno(1), 'Retorno de funciones',
                        'una función de tipo void no puede retornar un valor')
    #fin aporte Marcia Torres

    #Inicio aporte Mathias Giler: Función sin retorno
# Regla: función sin retorno
def p_declaracion_funcion_void(p):
    '''declaracion : funcion_void'''

# La cabecera se separa del cuerpo para que se reduzca antes de leer el cuerpo:
# así, al encontrar un return dentro, ya se sabe que la función es void
def p_funcion_void(p):
    '''funcion_void : cabecera_void cuerpo_base'''
    pila_funciones.pop()

def p_cabecera_void(p):
    '''cabecera_void : VOID ID PARENTESIS_IZQ parametros PARENTESIS_DER
                     | VOID ID PARENTESIS_IZQ PARENTESIS_DER'''
    tabla_funciones[p[2]] = 'void'
    pila_funciones.append('void')

# Regla: llamada a función o método como instrucción
def p_declaracion_llamada(p):
    '''declaracion : expresion PUNTO_COMA'''

# Regla: llamada a un método y acceso a una propiedad de un objeto
def p_expresion_metodo(p):
    '''expresion : expresion PUNTO ID PARENTESIS_IZQ elementos PARENTESIS_DER
                 | expresion PUNTO ID PARENTESIS_IZQ PARENTESIS_DER
                 | expresion PUNTO ID'''
    conversiones = {'toInt': 'int', 'toDouble': 'double', 'toString': 'String'}
    p[0] = conversiones.get(p[3]) if len(p) > 4 else None

    #fin aporte Mathias Giler

#Inicio aporte Mathias Giler: Impresión, solicitud de datos
# Regla: impresión
def p_declaracion_impresion(p):
    '''declaracion : impresion'''

def p_impresion(p):
    '''impresion : PRINT PARENTESIS_IZQ expresion PARENTESIS_DER PUNTO_COMA
                 | PRINT PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'''

# Regla: solicitud de datos por teclado
#   import 'dart:io';
#   String? [nombre] = stdin.readLineSync();
def p_declaracion_import(p):
    '''declaracion : IMPORT CADENA PUNTO_COMA'''

def p_expresion_lectura(p):
    '''expresion : STDIN PUNTO ID PARENTESIS_IZQ PARENTESIS_DER'''
    p[0] = 'String?'

# Tipo que acepta null (String?, int?) y el valor null
def p_tipo_nullable(p):
    '''tipo : tipo SIGNO_PREGUNTA'''
    p[0] = p[1] + '?'

def p_expresion_null(p):
    '''expresion : NULL'''
    p[0] = 'null'

    #fin aporte Mathias Giler

#Inicio aporte Marcia Torres: Clases, propiedades y métodos
# Regla: definición de clase
#   class [Nombre] { [propiedades] [constructor] [métodos] }
def p_declaracion_clase(p):
    '''declaracion : clase'''

def p_clase(p):
    '''clase : CLASS ID LLAVE_IZQ miembros LLAVE_DER
             | CLASS ID LLAVE_IZQ LLAVE_DER'''

def p_miembros(p):
    '''miembros : miembro
                | miembros miembro'''

# Propiedades (como una declaración con tipo) y métodos (cualquier tipo de función)
def p_miembro(p):
    '''miembro : tipado_explicito
               | funcion_retorno
               | lambda
               | funcion_void
               | constructor'''

# Regla: constructor
#   [Nombre](this.[propiedad], ...);
def p_constructor(p):
    '''constructor : ID PARENTESIS_IZQ parametros_constructor PARENTESIS_DER PUNTO_COMA
                   | ID PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'''

def p_parametros_constructor(p):
    '''parametros_constructor : THIS PUNTO ID
                              | parametros_constructor COMA THIS PUNTO ID'''

# Acceso a una propiedad dentro de la clase: this.[propiedad]
def p_expresion_this(p):
    '''expresion : THIS PUNTO ID'''

# Regla: crear un objeto de una clase
#   [Clase] [nombre] = [Clase]([argumentos]);
def p_declaracion_objeto(p):
    '''declaracion : ID ID ASIGNACION expresion PUNTO_COMA'''
#fin aporte Marcia Torres
parser = yacc.yacc()