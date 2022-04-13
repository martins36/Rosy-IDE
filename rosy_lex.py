# '''
#     rosy_yacc.py - Tokens para archivos .rosy de Rosy IDE
#     Creado por M. Macoritto, Septiembre 2021.
#     Licencia Pública General de GNU (GPL) versión 3.
# '''

import ply.lex as lex
from tkinter.messagebox import showwarning

'''---- DECLARACION DE TOKENS ----'''
tokens = [
    'DECIMAL',
    'ENTERO',
    'BINARY',
    'CADENA',
    'ID',
    'COMA',
    'PUNTO',
    'ASIGNACION',
    'MAS',
    'MENOS',
    'BARRA',
    'ASTERISCO',
    'MOD',
    'MAYOR',
    'MENOR',
    'MAYOR_IGUAL',
    'MENOR_IGUAL',
    'DISTINTO',
    'IGUAL',
    'PAREN_IZQ',
    'PAREN_DER',
    'SOMBRERITO'
]

reserved = {
    'DELAY' : 'DELAY',
    'PRINT' : 'PRINT',
    'GLOBAL' : 'GLOBAL',
    'CONST' : 'CONST',
    'TRUE' : 'TRUE',
    'FALSE' : 'FALSE',
    'FUNCTION' : 'FUNCTION',
    'METHOD' : 'METHOD',
    'RETURN' : 'RETURN',
    'THEN' : 'THEN',
    'END' : 'END',
    'CALL' : 'CALL',
    'WITH' : 'WITH',
    'TO' : 'TO',
    'IN' : 'IN',
    'RANGE' : 'RANGE',
    'FROM' : 'FROM',

    # Operaciones matematicas
    'ABS' : 'ABS',
    'MAX' : 'MAX',
    'MIN' : 'MIN',
    'SQRT' : 'SQRT',
    'MAP' : 'MAP',
    'COS' : 'COS',
    'SIN' : 'SIN',
    'TAN' : 'TAN',
    'RANDOM' : 'RANDOM',

    # Data type
    'STRING' : 'STRING',
    'INT' : 'INT',
    'LONG' : 'LONG',
    'BYTE' : 'BYTE',
    'CHAR' : 'CHAR',
    'FLOAT' : 'FLOAT',
    'BOOLEAN' : 'BOOLEAN',

    # Bucles
    'IF' : 'IF',
    'ELSE' : 'ELSE',
    'ELIF' : 'ELIF',
    'NOT' : 'NOT',
    'AND' : 'AND',
    'OR' : 'OR',
    'DO' : 'DO',
    'WHILE' : 'WHILE',
    'FOR' : 'FOR',
    'DECREMENT' : 'DECREMENT',

    # Propios
    'SOFT' : 'SOFT',
    'PLUS' : 'PLUS',
    'TIMES' : 'TIMES',
    'ALL' : 'ALL',

    # TOKENS AZULES
    'HIGH' : 'HIGH',
    'LOW' : 'LOW',
    'READ' : 'READ',
    'WRITE' : 'WRITE',
    'NO' : 'NO',
    'TONE' : 'TONE',
    'PULSE' : 'PULSE',

    # Propios
    'DISTANCE' : 'DISTANCE',
    'X_AXIS' : 'X_AXIS',
    'Y_AXIS' : 'Y_AXIS',
    'PUSH' : 'PUSH',
    'ANGLE' : 'ANGLE',
    'ROTATE' : 'ROTATE',
    'SOUNDING' : 'SOUNDING',
    'SCOREBOARD' : 'SCOREBOARD',
    'NUMBER' : 'NUMBER',
    'DOT' : 'DOT',
    'COLUMN' : 'COLUMN',
    'ROW' : 'ROW',
    'TEXT' : 'TEXT',
    'CLEAR' : 'CLEAR',
}

tokens += reserved

'''---- DEFINICION DE TOKENS -----'''
t_COMA = r'\,'
t_PUNTO = r'\.'
t_ASIGNACION = r'\='
t_MAS = r'\+'
t_MENOS = r'\-'
t_BARRA = r'/'
t_ASTERISCO = r'\*'
t_MOD = r'\%'
t_MAYOR = r'\>'
t_MENOR = r'\<'
t_MAYOR_IGUAL = r'\>='
t_MENOR_IGUAL = r'\<='
t_DISTINTO = r'\<>'
t_IGUAL = r'\=='
t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'
t_SOMBRERITO = r'\^'
t_ignore_WHITESPACES = r'[ \t]+'
t_ignore = ' \t'


def t_DECIMAL(token):
    r'\b([0-9]+[.])[0-9]+\b'
    return token


def t_ENTERO(token):
    r'\b[0-9]+\b'
    return token


def t_BINARY(token):
    r'\bB[01][01][01][01][01][01][01][01]\b'
    return token


def t_CADENA(token):
    r'[\"][^"\n]*[\"]|[\'][^\'\n]*[\']'
    return token


def t_ID(token):
    r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'
    token.type = reserved.get(token.value, 'ID')
    return token


def t_commentario(t):
    r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
    t.lexer.lineno += t.value.count('\n')


def t_error(token):
    showwarning(
        title='Advertencia',
        message=("Caracter ilegal '%s' en la línea %s" % (token.value[0], token.lexer.lineno))
    )
    token.lexer.skip(1)


def t_newline(token):
    r'\n'
    token.lexer.lineno += 1


'''------ CREACION DE LEXER ------'''
lexer = lex.lex()

'''------ ----------------- ------'''


def rosy_reset_lineno():
    lex.lex().lineno = 1
