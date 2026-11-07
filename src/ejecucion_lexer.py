import sys, os
from datetime import datetime
from lexer_dart import lexer, errors

def ejecutar(ruta_dart, usuario):
    with open(ruta_dart, encoding='utf-8') as f:
        data = f.read()
    errors.clear()
    lexer.lineno = 1
    lexer.input(data)

    marca = datetime.now().strftime('%d-%m-%Y-%Hh%M')
    os.makedirs('logs', exist_ok=True)
    ruta_log = f'logs/lexico-{usuario}-{marca}.txt'

    with open(ruta_log, 'w', encoding='utf-8') as out:
        out.write(f'Archivo: {ruta_dart}\nUsuario: {usuario}\n\n')
        for tok in lexer:
            out.write(f'L{tok.lineno:>3}  {tok.type:<15} {tok.value!r}\n')
        out.write(f'\nErrores léxicos: {len(errors)}\n')
        for linea, car in errors:
            out.write(f'  Línea {linea}: carácter no reconocido {car!r}\n')
    print('Log generado:', ruta_log)

if __name__ == '__main__':
    ejecutar(sys.argv[1], sys.argv[2])