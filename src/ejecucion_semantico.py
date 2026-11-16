import sys, os
from datetime import datetime
from lexer_dart import lexer
from parser_dart import parser, errores_sintacticos, errores_semanticos, reiniciar_semantico

def ejecutar(ruta_dart, usuario):
    with open(ruta_dart, encoding='utf-8') as f:
        data = f.read()
    errores_sintacticos.clear()
    reiniciar_semantico()
    lexer.lineno = 1
    parser.parse(data, lexer=lexer)

    marca = datetime.now().strftime('%d-%m-%Y-%Hh%M')
    os.makedirs('logs', exist_ok=True)
    ruta_log = f'logs/semantico-{usuario}-{marca}.txt'
    with open(ruta_log, 'w', encoding='utf-8') as out:
        out.write(f'Archivo: {ruta_dart}\nUsuario: {usuario}\n\n')
        if errores_sintacticos:
            out.write(f'Aviso: el código tiene {len(errores_sintacticos)} error(es) sintáctico(s), '
                      'el análisis semántico puede estar incompleto.\n\n')
        if errores_semanticos:
            for linea, categoria, msg in errores_semanticos:
                out.write(f'Error semántico ({categoria}) en línea {linea}: {msg}\n')
        else:
            out.write('No se encontraron errores semánticos.\n')
        out.write(f'\nErrores semánticos: {len(errores_semanticos)}\n')
    print('Log generado:', ruta_log)

if __name__ == '__main__':
    ejecutar(sys.argv[1], sys.argv[2])