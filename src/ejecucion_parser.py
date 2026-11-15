import sys, os
from datetime import datetime
from parser_dart import parser, errores_sintacticos
from lexer_dart import lexer

def ejecutar(ruta_dart, usuario):
    with open(ruta_dart, encoding='utf-8') as f:
        data = f.read()
    errores_sintacticos.clear()
    lexer.lineno = 1
    parser.parse(data, lexer=lexer)
    marca = datetime.now().strftime('%d-%m-%Y-%Hh%M')
    os.makedirs('logs', exist_ok=True)
    ruta_log = f'logs/sintactico-{usuario}-{marca}.txt'
    with open(ruta_log, 'w', encoding='utf-8') as out:
        out.write(f'Archivo: {ruta_dart}\nUsuario: {usuario}\n\n')
        if errores_sintacticos:
            for linea, msg in errores_sintacticos:
                if linea is None:
                    out.write(f'Error de sintaxis: {msg}\n')
                else:
                    out.write(f'Error de sintaxis en línea {linea}: {msg}\n')
        else:
            out.write('No se encontraron errores sintácticos.\n')
        out.write(f'\nErrores sintácticos: {len(errores_sintacticos)}\n')
    print('Log generado:', ruta_log)
if __name__ == '__main__':
    ejecutar(sys.argv[1], sys.argv[2])