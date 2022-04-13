# '''
#     pini_yacc.py - Gramatica para archivos .pini de Rosy IDE
#     Creado por M. Macoritto, Septiembre 2021.
#     Licencia Pública General de GNU (GPL) versión 3.
# '''

import ply.yacc as yacc
from pini_lex import tokens
from pini_lex import pini_reset_lineno
from tkinter.messagebox import showerror

void = ""
pini_error = False
digital_variables = []
analog_variables = []
includes = []

'''------ DECLARACION DE REGLAS ------'''


def p_start(p):
    '''start : pin_digital start
             | pin_analog start
             | ultrasonic start
             | joystick start
             | servo start
             | display start
             | matrix start
             | empty'''
    if len(p) >= 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""


def p_pin_digital(p):
    'pin_digital : PIN DIGITAL COMA ID COMA io'
    p[0] = "#define " + p[4] + " " + p[2] + "\n"
    global void
    global digital_variables
    void += "  pinMode(" + p[4] + ", " + p[6] + ");\n"
    digital_variables.append(p[4])


def p_io(p):
    '''io : OUT
          | INP
          | INP_PUL'''
    if p[1] == "OUT":
        p[0] = "OUTPUT"
    elif p[1] == "INP":
        p[0] = "INPUT"
    elif p[1] == "INP_PUL":
        p[0] = "INPUT_PULLUP"


def p_pin_analog(p):
    'pin_analog : PIN ANALOG COMA ID'
    p[0] = "#define " + p[4] + " " + p[2] + "\n"
    global analog_variables
    analog_variables.append(p[4])


def p_ultrasonic(p):
    'ultrasonic : ULTRASONIC DIGITAL COMA DIGITAL COMA ID'
    p[0] = "int " + p[6] + "[] = {" + p[2] + ", " + p[4] + "};\n"
    global void
    void += (
        "  pinMode(" + p[2] + ", OUTPUT);\n" +
        "  pinMode(" + p[4] + ", INPUT);\n"
    )


def p_joystick(p):
    'joystick : JOYSTICK ANALOG COMA ANALOG COMA DIGITAL COMA ID'
    p[0] = "int " + p[8] + "[] = {" + p[2] + ", " + p[4] + ", " + p[6] + "};\n"
    global void
    void += "  pinMode(" + p[6] + ", INPUT_PULLUP);\n"


def p_servo(p):
    'servo : SERVO DIGITAL COMA ID'
    p[0] = "Servo " + p[4] + ";\n"
    global void
    global includes
    includes.append("#include <Servo.h>\n")
    void += "  " + p[4] + ".attach(" + p[2] + ");\n"


def p_display(p):
    'display : DISPLAY DIGITAL COMA DIGITAL COMA ID intensity_display'
    p[0] = "TM1637 " + p[6] + "(" + p[2] + ", " + p[4] + ");\n"
    global void
    global includes
    includes.append("#include <TM1637.h>\n")
    if p[7] == "":
        void += "  " + p[6] + ".set(3);\n"
    else:
        void += "  " + p[6] + p[7]


def p_intensity_display(p):
    '''intensity_display : COMA INTENSITY number
                         | empty'''
    if len(p) >= 3:
        p[0] = ".set(" + p[3] + ");\n"
    else:
        p[0] = ""


def p_matrix(p):
    'matrix : MATRIX number COMA DIGITAL COMA DIGITAL COMA DIGITAL COMA ID intensity_matrix'
    p[0] = "LedControl " + p[10] + " = LedControl(" + p[4] + ", " + p[6] + ", " + p[8] + ", " + p[2] + ");\n"
    global void
    global includes
    includes.append("#include <LedControlMS.h>\n")
    intensity = "8"
    if p[11] != "":
        intensity = p[11]

    void += (
        "  for (int i = 0; i < " + p[2] + " ; i++) {\n"
        "    " + p[10] + ".shutdown(i, false);\n"
        "    " + p[10] + ".setIntensity(i, " + intensity + ");\n"
        "    " + p[10] + ".clearDisplay(i);\n"
        "  }\n"
    )


def p_intensity_matrix(p):
    '''intensity_matrix : COMA INTENSITY number
                        | empty'''
    if len(p) >= 3:
        p[0] = p[3]
    else:
        p[0] = ""


def p_number(p):
    '''number : DIGITAL
              | ENTERO'''
    p[0] = p[1]


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    global pini_error
    pini_error = True
    message = ""
    if p != None:
        message = "Error de sintaxis en Pini: línea %s" % p.lineno
    else:
        message = "Unexpected end of input in Pini"

    showerror(title='Fallo al compilar', message=message)


'''------- CREACION DE PARSER --------'''
parser = yacc.yacc()

'''-------- ----------------- --------'''


def pini_compile(text):
    global void
    global pini_error
    global digital_variables
    global analog_variables
    global includes

    void = ""
    pini_error = False
    digital_variables.clear()
    analog_variables.clear()
    includes.clear()
    pini_reset_lineno()

    result = parser.parse(text)

    if result is not None and not pini_error:
        result += "\nvoid setup()\n{\n" + void + "  Serial.begin(9600);\n}\n"

        includes = list(dict.fromkeys(includes))
        for i in includes:
            result = i + result

    return result
