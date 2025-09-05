#!/usr/bin/env python3
import argparse
import sys

def caesar_encrypt(text: str, shift: int) -> str:
    """
    Cifra `text` usando el cifrado César con desplazamiento `shift`.
    - Sólo rota letras ASCII A-Z y a-z (preserva mayúsculas/minúsculas).
    - Caracteres no alfabéticos se dejan sin cambiar (espacios, signos, acentos, ñ quedan tal cual).
    """
    result = []
    shift = shift % 26  # acotar al rango 0-25
    for ch in text:
        if 'a' <= ch <= 'z':
            result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= ch <= 'Z':
            result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(ch)
    return ''.join(result)

def main():
    parser = argparse.ArgumentParser(description="Cifrado César (Python 3)")
    parser.add_argument('text', nargs='?', help='Texto a cifrar (si tiene espacios, encerrar entre comillas)')
    parser.add_argument('shift', nargs='?', type=int, help='Desplazamiento entero (p.ej. 3)')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Descifrar: aplica desplazamiento negativo')
    args = parser.parse_args()

    if args.text is None or args.shift is None:
        try:
            text = input("Texto a cifrar: ")
            shift = int(input("Desplazamiento (entero): "))
        except Exception as e:
            print("Entrada inválida:", e, file=sys.stderr)
            sys.exit(1)
    else:
        text = args.text
        shift = args.shift

    if args.decrypt:
        shift = -shift

    encrypted = caesar_encrypt(text, shift)
    print(encrypted)

if __name__ == '__main__':
    main()
