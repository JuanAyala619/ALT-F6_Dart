#Formato base
import ply.lex as lex

reserved = {

}
# List of token names. This is always required
tokens = (
    #Tokens a implementar: 
    #Juan
    'ID','ENTERO','DECIMAL','SUMA','RESTA','MULTIPLICACION','DIVISION',
    'DIV_ENTERA','MODULO','INCREMENTO','DECREMENTO',
    'CORCHETE_IZQ','CORCHETE_DER','FLECHA',
    #Marcia
    'CADENA','MENOR_QUE','MAYOR_QUE','MENOR_IGUAL','MAYOR_IGUAL','IGUAL','DIFERENTE',
    'AND','OR','NOT', 'ASIGNACION', 'ASIGNACION_NULL','LLAVE_IZQ','LLAVE_DER',
    #Mathias
    'PARENTESIS_IZQ','PARENTESIS_DER','PUNTO_COMA','COMA',
    'PUNTO','DOS_PUNTOS','SIGNO_PREGUNTA'
) + tuple(reserved.values())
