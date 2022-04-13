# '''
#     pini_lex.py - Tokens para archivos .pini de Rosy IDE
#     Creado por M. Macoritto, Septiembre 2021.
#     Licencia Pública General de GNU (GPL) versión 3.
#
#     Pines digitales y analogicos de cada placa Arduino:
#     - Mega ([2-9]|[1234][0-9]) y [A]([0-9]|[1][0-5])
#       rango:  2  - 49             A0 - A15
#
#     - Uno ([2-9]|[1][0-3]) y [A]([0-5])
#       rango:  2  - 13         A0 - A5
#
#     - Nano ([2-9]|[1][0-3]) y [A]([0-7])
#       rango:  2  - 13          A0 - A7
# '''

import ply.lex as lex
from tkinter.messagebox import showwarning

'''---- DECLARACION DE TOKENS ----'''
tokens = [
    'DIGITAL',
    'ANALOG',
    'ID',
    'ENTERO',
    'COMA'
]

reserved = {
    'PIN' : 'PIN',
    'OUT' : 'OUT',
    'INP' : 'INP',
    'INP_PUL' : 'INP_PUL',
    'ULTRASONIC' : 'ULTRASONIC',
    'JOYSTICK' : 'JOYSTICK',
    'SERVO' : 'SERVO',
    'DISPLAY' : 'DISPLAY',
    'MATRIX' : 'MATRIX',
    'INTENSITY' : 'INTENSITY'
}

tokens += reserved

'''---- DEFINICION DE TOKENS -----'''
t_COMA = r'\,'
t_ignore_WHITESPACES = r'[ \t]+'
t_ignore = ' \t'


def t_DIGITAL(token):
    r'\b([2-9]|[1][0-3])\b'
    return token


def t_ANALOG(token):
    r'\b[A]([0-5])\b'
    return token


def t_ID(token):
    r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'
    token.type = reserved.get(token.value, 'ID')
    return token


def t_ENTERO(token): # de 0 a 15
    r'\b([0-9]|[1][0-5])\b'
    return token


def t_commentario(t):
    r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
    t.lexer.lineno += t.value.count('\n')


def t_error(token):
    showwarning(
        title='Advertencia',
        message=("Caracter ilegal '%s' en Pini: líena %s" % (token.value[0], token.lexer.lineno))
    )
    token.lexer.skip(1)


def t_newline(token):
    r'\n'
    token.lexer.lineno += 1


'''------ CREACION DE LEXER ------'''
lexer = lex.lex()


def pini_reset_lineno():
    lex.lex().lineno = 1
