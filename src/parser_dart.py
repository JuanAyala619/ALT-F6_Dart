import ply.yacc as yacc
from lexer_dart import tokens

errores_sintacticos = []
start = 'programa'

def p_programa(p):
    '''programa : declaraciones'''

# Inicio aporte Juan Ayala (JuanAyala619): reglas de precedencia 

# fin aporte Juan Ayala
#Declaración de variables
    #Inicio aporte Juan Ayala: Tipado explícito

    #fin aporte Juan Ayala
    #Inicio aporte Marcia Torres (marciatorresg): Tipado inferido

    #fin aporte Marcia Torres

    #Inicio aporte Mathias Giler (matheoglg): Constante en tiempo de compilación

    #fin aporte Mathias Giler

#Inicio aporte Juan Ayala: Expresiones aritméticas

#fin aporte Juan Ayala

#Inicio aporte Marcia Torres: Expresiones booleanas

#fin aporte Marcia Torres

#Estructuras de Control
    #Inicio aporte Juan Ayala: Bucle while

    #fin aporte Juan Ayala
    #Inicio aporte Marcia Torres: if-else

    #fin aporte Marcia Torres

    #Inicio aporte Mathias Giler: Bucle for

    #fin aporte Mathias Giler
#Estructuras de datos
    #Inicio aporte Juan Ayala: Listas

    #fin aporte Juan Ayala
    #Inicio aporte Marcia Torres: Conjuntos

    #fin aporte Marcia Torres
    #Inicio aporte Mathias Giler: Tuplas/Records

    #fin aporte Mathias Giler
#Declaraciones de funciones
    #Inicio aporte Juan Ayala: Lambda

    #fin aporte Juan Ayala
    #Inicio aporte Marcia Torres: Función con retorno

    #fin aporte Marcia Torres
    #Inicio aporte Mathias Giler: Función sin retorno

    #fin aporte Mathias Giler
#Inicio aporte Mathias Giler: Impresión, solicitud de datos y manejo de errores

    #fin aporte Mathias Giler
#parser = yacc.yacc()   # activar cuando exista la base (declaraciones, tipo, expresion)