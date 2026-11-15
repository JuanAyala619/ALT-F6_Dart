import ply.yacc as yacc
from lexer_dart import tokens

errores_sintacticos = []
start = 'programa'

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

def p_expresion(p):
    '''expresion : ENTERO
                | DECIMAL
                | CADENA
                | TRUE
                | FALSE
                | ID
                | PARENTESIS_IZQ expresion PARENTESIS_DER
                | operacion_aritmetica'''
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
# fin aporte Juan Ayala
#Declaración de variables
    #Inicio aporte Juan Ayala: Tipado explícito
def p_declaracion_tipado_explicito(p):
    '''declaracion : tipado_explicito'''

def p_tipado_explicito(p):
    '''tipado_explicito : tipo ID ASIGNACION expresion PUNTO_COMA
                        | tipo ID PUNTO_COMA'''
    #fin aporte Juan Ayala
    #Inicio aporte Marcia Torres (marciatorresg): Tipado inferido

    #fin aporte Marcia Torres

#Inicio aporte Mathias Giler (matheoglg): Constante en tiempo de compilación
def p_declaracion_constante(p):
    '''declaracion : constante'''

def p_constante(p):
    '''constante : CONST tipo ID ASIGNACION expresion PUNTO_COMA 
                | CONST ID ASIGNACION expresion PUNTO_COMA
                | FINAL tipo ID ASIGNACION expresion PUNTO_COMA
                | FINAL ID ASIGNACION expresion PUNTO_COMA'''
    #fin aporte Mathias Giler

#Inicio aporte Juan Ayala: Expresiones aritméticas
def p_declaracion_asignacion(p):
    '''declaracion : asignacion'''

def p_asignacion(p):
    '''asignacion : ID ASIGNACION expresion PUNTO_COMA'''

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
#fin aporte Juan Ayala

#Inicio aporte Marcia Torres: Expresiones booleanas

#fin aporte Marcia Torres

#Estructuras de Control
    #Inicio aporte Juan Ayala: Bucle while
def p_declaracion_bucle_while(p):
    '''declaracion : bucle_while'''
def p_bucle_while(p):
    '''bucle_while : WHILE PARENTESIS_IZQ expresion PARENTESIS_DER cuerpo_base'''
    #fin aporte Juan Ayala
    #Inicio aporte Marcia Torres: if-else

    #fin aporte Marcia Torres

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
def p_elementos(p):
    '''elementos : expresion
                | elementos COMA expresion'''  
def p_expresion_acceso_lista(p):
    '''expresion : ID CORCHETE_IZQ expresion CORCHETE_DER'''      

    #fin aporte Juan Ayala
    #Inicio aporte Marcia Torres: Conjuntos

    #fin aporte Marcia Torres
    #Inicio aporte Mathias Giler: Tuplas/Records

    #fin aporte Mathias Giler
#Declaraciones de funciones
    #Inicio aporte Juan Ayala: Lambda
def p_declaracion_lambda(p):
    '''declaracion : lambda'''
def p_lambda(p):
    '''lambda : tipado_comun FLECHA expresion PUNTO_COMA'''
def p_tipado_comun(p):
    '''tipado_comun : tipo ID PARENTESIS_IZQ parametros PARENTESIS_DER
                    | tipo ID PARENTESIS_IZQ PARENTESIS_DER'''
def p_parametros(p):
    '''parametros : tipo ID 
                | parametros COMA tipo ID'''
def p_expresion_llamada_funcion(p):
    '''expresion : ID PARENTESIS_IZQ elementos PARENTESIS_DER
                 | ID PARENTESIS_IZQ PARENTESIS_DER'''
    #fin aporte Juan Ayala
    #Inicio aporte Marcia Torres: Función con retorno

    #fin aporte Marcia Torres
    #Inicio aporte Mathias Giler: Función sin retorno

    #fin aporte Mathias Giler
#Inicio aporte Mathias Giler: Impresión, solicitud de datos

    #fin aporte Mathias Giler
parser = yacc.yacc()   