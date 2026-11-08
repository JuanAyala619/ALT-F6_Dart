#Formato base
import ply.lex as lex

reserved = {
    #Inicio aporte Juan Ayala (JuanAyala619): abstract - extension
    "abstract": "ABSTRACT",
	"as": "AS",
	"assert": "ASSERT",
	"async": "ASYNC",
    "await": "AWAIT",
    "base": "BASE",
    "break": "BREAK",
    "case": "CASE",
    "catch": "CATCH",
    "class": "CLASS",
    "const": "CONST",
    "continue": "CONTINUE",
    "covariant": "COVARIANT",
    "default": "DEFAULT",
    "deferred": "DEFERRED",
    "do": "DO",
    "dynamic": "DYNAMIC",
    "else": "ELSE",
    "enum": "ENUM",
    "export": "EXPORT",
    "extends": "EXTENDS",
    "extension": "EXTENSION",
    #tipos y print
    "int": "INT",
    "double": "DOUBLE",
    "String": "STRING",
    "bool": "BOOL",
    "List": "LIST",
    "Set": "SET",
    "print": "PRINT",
    #fin aporte Juan Ayala
    #Inicio aporte Marcia Torres (marciatorresg): external - on

    #fin aporte Marcia Torres
    #Inicio aporte Mathias Giler (matheoglg): operator - yield
    "operator": "OPERATOR",
    "part": "PART",
    "required": "REQUIRED",
    "rethrow": "RETHROW",
    "return": "RETURN",
    "sealed": "SEALED",
    "set": "SETTER",
    "show": "SHOW",
    "static": "STATIC",
    "super": "SUPER",
    "switch": "SWITCH",
    "sync": "SYNC",
    "this": "THIS",
    "throw": "THROW",
    "true": "TRUE",
    "try": "TRY",
    "type": "TYPE",
    "typedef": "TYPEDEF",
    "var": "VAR",
    "void": "VOID",
    "when": "WHEN",
    "with": "WITH",
    "while": "WHILE",
    "yield": "YIELD",
    #fin aporte Mathias Giler
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

#Inicio aporte Juan Ayala: aritméticos, corchetes y flecha
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_DIV_ENTERA = r'~/'
t_MODULO = r'%'
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'--'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_FLECHA = r'=>'
#Fin aporte Juan Ayala
#Inicio aporte Marcia Torres: Cadenas

#fin aporte Marcia Torres

#Inicio aporte Mathias Giler: comentarios
def t_COMENTARIO_DOC(t):
    r'///[^\n]*'
    pass

def t_COMENTARIO_LINEA(t):
    r'//[^\n]*'
    pass

def t_COMENTARIO_BLOQUE(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
#fin aporte Mathias Giler

#Inicio aporte Juan Ayala: ID y números
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_DECIMAL(t):
    r'\d+\.\d+([eE][-+]?\d+)?|\d+[eE][-+]?\d+'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t
#Fin aporte Juan Ayala
#Inicio aporte Marcia Torres: relacionales, lógicos, asignación y llaves

#fin aporte Marcia Torres
#Inicio aporte Mathias Giler: delimitadores, newline, ignore, errors y construcción lexer

#fin aporte Mathias Giler