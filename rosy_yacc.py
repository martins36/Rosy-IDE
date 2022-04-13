# '''
#     pini_yacc.py - Gramatica para archivos .rosy de Rosy IDE
#     Creado por M. Macoritto, Abril 2022.
#     Licencia Pública General de GNU (GPL) versión 3.
# '''

import ply.yacc as yacc
from rosy_lex import tokens
from rosy_lex import rosy_reset_lineno
from pini_yacc import pini_compile
from pini_yacc import digital_variables
from pini_yacc import analog_variables
from tkinter.messagebox import showerror, showinfo

from utils import absolute

globals = ""
functions_methods = "\n"
rosy_error = False

distance_method = True
sounding_function = True
scoreboard_function = True
scoreboard_plus_function = True
number_function = True
text_function = True

'''------ DECLARACION DE REGLAS ------'''


def p_start(p):
    'start : globals functions_methods body'
    p[0] = "\n" + p[3]


def p_globals(p):
    '''globals : global_variable globals
               | empty'''
    pass


def p_functions_methods(p):
    '''functions_methods : function functions_methods
                         | method functions_methods
                         | empty'''
    pass


def p_function(p):
    'function : FUNCTION ID COMA fm_parameters THEN body END FUNCTION'
    global functions_methods
    functions_methods += "\nvoid " + p[2] + "(" + p[4] + ")\n{\n" + p[6] + "}\n"
    pass


def p_method(p):
    'method : METHOD ID COMA fm_parameters RETURN data_type COMA THEN body RETURN alguito END METHOD'
    global functions_methods
    functions_methods += "\n" + p[6] + " " + p[2] + "(" + p[4] + ")\n{\n" + p[9] + "  return " + p[11] + ";\n}\n"
    pass


def p_body(p):
    '''body : digital_write body
            | analog_write body
            | delay body
            | tone body
            | no_tone body
            | rotate body
            | sounding body
            | scoreboard body
            | number_dspy body
            | clear_dspy body
            | dot body
            | row body
            | column body
            | text_matrix body
            | clear_matrix body
            | asignacion body
            | asignacion_variable body
            | const_variable body
            | call_function_method body
            | print body
            | for body
            | while body
            | do_while body
            | if body
            | empty'''
    if len(p) >= 3:
        p[0] = "  " + p[1] + ";\n" + p[2]
    else:
        p[0] = ""


def p_asignacion(p):
    'asignacion : ID ASIGNACION algo'
    p[0] = p[1] + " " + p[2] + " " + p[3]


def p_asignacion_variable(p):
    'asignacion_variable : data_type asignacion'
    p[0] = p[1] + " " + p[2]


def p_const_variable(p):
    'const_variable : CONST asignacion_variable'
    p[0] = "const " + p[2]


def p_global_variable(p):
    '''global_variable : GLOBAL asignacion_variable
                       | GLOBAL const_variable'''
    global globals
    globals += p[2] + ";\n"
    pass


def p_call_function_method(p):
    'call_function_method : CALL ID cfm_arguments'
    p[0] = p[2] + "(" + p[3] + ")"


def p_print(p):
    'print : PRINT alguito concatenate_print'
    p[0] = "Serial.print(" + p[2] + ");" + p[3]


def p_concatenate_print(p):
    '''concatenate_print : COMA alguito concatenate_print
                         | empty'''
    if len(p) == 4:
        p[0] = "\n  Serial.print(" + p[2] + ");" + p[3]
    else:
        p[0] = "\n  Serial.println()"


# CICLOS CONDICIONALES


def p_for(p):
    'for : FOR ID IN RANGE ENTERO COMA ENTERO COMA decrement THEN body END FOR'
    if p[9] == "DECREMENT":
        p[0] = "for (int " + p[2] + " = " + p[7] + "; " + p[2] + " > " + p[5] + "; " + p[2] + "--) {\n  " + p[11].replace("\n", "\n  ") + "}"
    else:
        p[0] = "for (int " + p[2] + " = " + p[5] + "; " + p[2] + " < " + p[7] + "; " + p[2] + "++) {\n  " + p[11].replace("\n", "\n  ") + "}"


def p_while(p):
    'while : WHILE logic COMA THEN body END WHILE'
    p[0] = "while (" + p[2] + ") {\n  " + p[5].replace("\n", "\n  ") + "}"


def p_do_while(p):
    'do_while : DO WHILE logic COMA THEN body END DO WHILE'
    p[0] = "do {\n  " + p[6].replace("\n", "\n  ") + "} while (" + p[3] + ")"


def p_if(p):
    'if : IF logic COMA THEN body END IF elseif else'
    p[0] = "if (" + p[2] + ") {\n  " + p[5].replace("\n", "\n  ") + "}" + p[8] + p[9]


def p_elseif(p):
    '''elseif : ELIF logic COMA THEN body END ELIF elseif
              | empty'''
    if len(p) >= 3:
        p[0] = "\n  else if (" + p[2] + ") {\n  " + p[5].replace("\n", "\n  ") + "}" + p[8]
    else:
        p[0] = ""


def p_else(p):
    '''else : ELSE body END ELSE
            | empty'''
    if len(p) >= 3:
        p[0] = "\n  else {\n  " + p[2].replace("\n", "\n  ") + "}"
    else:
        p[0] = ""


# FUNCIONES EXCLUSIVAS DE ARDUINO


def p_read(p):
    'read : ID PUNTO READ'
    global digital_variables
    global analog_variables

    digital = False
    analog = False
    for i in digital_variables:
        if i == p[1]:
            digital = True
            break
    if digital:
        p[0] = "digitalRead(" + p[1] + ")"
    else:
        for i in analog_variables:
            if i == p[1]:
                analog = True
                break
        if analog:
            p[0] = "analogRead(" + p[1] + ")"
        else:
            p[0] = "0; // Error: variable inexistete"


def p_digital_write(p):
    'digital_write : ID PUNTO value'
    p[0] = "digitalWrite(" + p[1] + ", " + p[3] + ")"


def p_analog_write(p):
    'analog_write : ID PUNTO WRITE expression'
    p[0] = "analogWrite(" + p[1] + ", " + p[4] + ")"


def p_delay(p):
    'delay : DELAY number'
    p[0] = "delay(" + str(int(float(p[2]) * 1000)) + ")"


def p_tone(p):
    '''tone : ID PUNTO TONE alguito
            | ID PUNTO TONE alguito COMA number'''
    if len(p) == 5:
        p[0] = "tone(" + p[1] + ", " + p[4] + ")"
    else:
        p[0] = "tone(" + p[1] + ", " + p[4] + ", " + str(int(float(p[6]) * 1000)) + ")"


def p_no_tone(p):
    'no_tone : ID PUNTO NO TONE'
    p[0] = "noTone(" + p[1] + ")"


def p_pulse(p):
    '''pulse : ID PUNTO PULSE value
             | ID PUNTO PULSE value COMA number'''
    if len(p) == 5:
        p[0] = "pulseIn(" + p[1] + ", " + p[4] + ")"
    else:
        p[0] = "pulseIn(" + p[1] + ", " + p[4] + ", " + str(int(float(p[6]) * 1000)) + ")"


# FUNCIONES PROPIAS (que yo desarrolle) DE ARDUINO


def p_distance(p): #ULTRASONICO: devuelve la ditancia del ultrasonico en cm
    'distance : ID PUNTO DISTANCE'
    p[0] = "DISTANCE(" + p[1] + ")"
    global functions_methods
    global distance_method
    if distance_method:
        functions_methods += (
            "\nint DISTANCE(int arr[])\n" +
            "{\n" +
            "  digitalWrite(arr[0], LOW);\n" +
            "  delayMicroseconds(5);\n" +
            "  digitalWrite(arr[0], HIGH);\n" +
            "  delayMicroseconds(10);\n" +
            "  digitalWrite(arr[0], LOW);\n" +
            "  return (pulseIn(arr[1], HIGH) / 58.2);\n" +
            "}\n"
        )
        distance_method = False


def p_x_axis(p): #JOYSTICK
    'x_axis : ID PUNTO X_AXIS'
    p[0] = "analogRead(" + p[1] + "[0])"


def p_y_axis(p): #JOYSTICK
    'y_axis : ID PUNTO Y_AXIS'
    p[0] = "analogRead(" + p[1] + "[1])"


def p_push(p): #JOYSTICK
    'push : ID PUNTO PUSH'
    p[0] = "digitalRead(" + p[1] + "[2])"


def p_angle(p): #SERVO: devuelve el angulo del servo (entre 0 y 180)
    'angle : ID PUNTO ANGLE'
    p[0] = p[1] + ".read()"


def p_rotate(p): #SERVO
    'rotate : ID PUNTO ROTATE ENTERO'
    p[0] = p[1] + ".write(" + p[4] + ")"


def p_sounding(p): #SERVO
    '''sounding : ID PUNTO SOUNDING ENTERO COMA ENTERO COMA ENTERO
                | ID PUNTO SOUNDING ENTERO COMA ENTERO COMA ENTERO COMA SOFT'''
    soft = "false"
    if len(p) == 11:
        soft = "true"
    p[0] = "SOUNDING(" + p[1] + ", " + p[4] + ", " + p[6] + ", " + p[8] + ", " + soft + ")"
    global functions_methods
    global sounding_function
    if sounding_function:
        functions_methods += (
            "\nvoid SOUNDING(Servo ser, int min, int max, int vel, bool soft)\n" +
            "{\n" +
            "  for (int i = min; i <= max; i++) {\n" +
            "    ser.write(i);\n" +
            "    delay(vel);\n" +
            "  }\n" +
            "  if (soft) {\n" +
            "    for (int i = max; i >= min; i--) {\n" +
            "      ser.write(i);\n" +
            "      delay(vel);\n" +
            "    }\n" +
            "  }\n" +
            "}\n"
        )
        sounding_function = False


def p_scoreboard(p): #DISPLAY4D
    '''scoreboard : ID PUNTO SCOREBOARD ENTERO COMA ENTERO
                  | ID PUNTO SCOREBOARD PLUS ENTERO COMA ENTERO'''
    global functions_methods
    if len(p) == 7:
        p[0] = "SCOREBOARD(" + p[1] + ", " + p[4] + ", " + p[6] + ")"
        global scoreboard_function
        if scoreboard_function:
            functions_methods += (
                "\nvoid SCOREBOARD(TM1637 d4d, int p1, int p2)\n" +
                "{\n" +
                "  d4d.init();\n" +
                "  d4d.point(POINT_ON);\n" +
                "  d4d.display(0, p1);\n" +
                "  d4d.display(3, p2);\n" +
                "}\n"
            )
            scoreboard_function = False
    else:
        p[0] = "SCOREBOARD_PLUS(" + p[1] + ", " + p[5] + ", " + p[7] + ")"
        global scoreboard_plus_function
        if scoreboard_plus_function:
            functions_methods += (
                "\nvoid SCOREBOARD_PLUS(TM1637 d4d, int p1, int p2)\n" +
                "{\n" +
                "  d4d.init();\n" +
                "  d4d.point(POINT_ON);\n" +
                "  d4d.display(0, p1 / 10);\n" +
                "  d4d.display(1, p1 % 10);\n" +
                "  d4d.display(2, p2 / 10);\n" +
                "  d4d.display(3, p2 % 10);\n" +
                "}\n"
            )
            scoreboard_plus_function = False


def p_number_dspy(p): #DISPLAY4D
    'number_dspy : ID PUNTO NUMBER ENTERO'
    p[0] = "NUMBER(" + p[1] + ", " + p[4] + ")"
    global functions_methods
    global number_function
    if number_function:
        functions_methods += (
            "\nvoid NUMBER(TM1637 d4d, int number)\n" +
            "{\n" +
            "  d4d.init();\n" +
            "  d4d.point(POINT_OFF);\n" +
            "  d4d.display(0, number / 1000);\n" +
            "  d4d.display(1, (number % 1000) / 100);\n" +
            "  d4d.display(2, ((number % 1000) % 100) / 10);\n" +
            "  d4d.display(3, (((number % 1000) % 100) % 10));\n" +
            "}\n"
        )
        number_function = False


def p_clear_dspy(p): #DISPLAY4D
    'clear_dspy : ID PUNTO CLEAR'
    p[0] = p[1] + ".init()"


def p_dot(p): #MATRIX
    'dot : ID PUNTO DOT ENTERO COMA ENTERO COMA IN ENTERO'
    p[0] = p[1] + ".setLed(" + str(int(p[9]) - 1) + ", " + str(int(p[4]) - 1) + ", " + str(int(p[6]) - 1) + ", true)"


def p_row(p): #MATRIX
    'row : ID PUNTO ROW ENTERO COMA BINARY COMA IN ENTERO'
    p[0] = p[1] + ".setColumn(" + str(int(p[9]) - 1) + ", " + str(int(p[4]) - 1) + ", " + p[6] + ")"


def p_column(p): #MATRIX
    'column : ID PUNTO COLUMN ENTERO COMA BINARY COMA IN ENTERO'
    p[0] = p[1] + ".setRow(" + str(int(p[9]) - 1) + ", " + str(int(p[4]) - 1) +", " + p[6] + ")"


def p_text_matrix(p): #MATRIX
    'text_matrix : ID PUNTO TEXT CADENA COMA ENTERO COMA ENTERO TIMES'
    p[0] = "TEXT(" + p[1] + ", " + p[4] + ", " + p[8] + ", " + p[6] + ")"
    global functions_methods
    global text_function
    if text_function:
        functions_methods += (
            "\nvoid TEXT(LedControl mlc, String text, int n, int numMatrix)\n" +
            "{\n" +
            "  char ch[numMatrix];\n" +
            "  int nextCharIndex = numMatrix;\n" +
            "  for (int i = 0; i < numMatrix; i++) {\n" +
            "    ch[i] = text[i];\n" +
            "    text += ' ';\n" +
            "  }\n" +
            "  while (n > 0) {\n" +
            "    for (int i = 0; i < numMatrix; i++) {\n" +
            "      mlc.displayChar(map(i, 0, numMatrix - 1, numMatrix - 1, 0), mlc.getCharArrayPosition(ch[i]));\n" +
            "    }\n" +
            "    for (int i = 0; i < numMatrix - 1; i++) {\n" +
            "      ch[i] = ch[i + 1];\n" +
            "    }\n" +
            "    ch[numMatrix - 1] = text[nextCharIndex++];\n" +
            "    if (nextCharIndex >= text.length()) {\n" +
            "      nextCharIndex = 0;\n" +
            "      n--;\n" +
            "    }\n" +
            "    delay(500);\n" +
            "    mlc.clearAll();\n" +
            "    delay(5);\n" +
            "  }\n" +
            "}\n"
        )
        text_function = False


def p_clear_matrix(p): #MATRIX
    '''clear_matrix : ID PUNTO CLEAR ENTERO
                    | ID PUNTO CLEAR ALL'''
    if p[3] == "ALL":
        p[0] = p[1] + ".clearAll()"
    else:
        p[0] = p[1] + ".clearDisplay(" + str(int(p[4]) - 1) + ")"


# FUNCIONES MATEMATICAS


def p_abs(p):
    'abs : ABS expression'
    p[0] = "abs(" + p[2] + ")"


def p_max(p):
    'max : MAX expression COMA expression'
    p[0] = "max(" + p[2] + ", " + p[4] + ")"


def p_min(p):
    'min : MIN expression COMA expression'
    p[0] = "min(" + p[2] + ", " + p[4] + ")"


def p_sqrt(p):
    'sqrt : SQRT expression'
    p[0] = "sqrt(" + p[2] + ")"


def p_cos(p):
    'cos : COS expression'
    p[0] = "cos(" + p[2] + ")"


def p_sin(p):
    'sin : SIN expression'
    p[0] = "sin(" + p[2] + ")"


def p_tan(p):
    'tan : TAN expression'
    p[0] = "tan(" + p[2] + ")"


def p_map(p):
    'map : MAP expression FROM expression COMA expression TO expression COMA expression'
    p[0] = "map(" + p[2] + ", " + p[4] +  ", " + p[6] + ", " + p[8] + ", " + p[10] + ")"


def p_random(p):
    '''random : RANDOM ENTERO
              | RANDOM IN RANGE ENTERO COMA ENTERO'''
    if len(p) == 3:
        p[0] = "random(" + p[2] + ")"
    else:
        p[0] = "random(" + p[4] + ", " + p[6] + ")"


# FUNCIONES AUXILIARES GENERALES


def p_algo(p):
    '''algo : alguito
            | pulse
            | abs
            | max
            | min
            | sqrt
            | cos
            | sin
            | tan
            | map
            | random
            | call_function_method'''
    p[0] = p[1]


def p_alguito(p):
    '''alguito : CADENA
               | read
               | distance
               | x_axis
               | y_axis
               | push
               | angle
               | boolean
               | expression'''
    p[0] = p[1]


def p_expression(p):
    '''expression : expression MENOS expression
                  | expression MAS expression
                  | expression BARRA expression
                  | expression ASTERISCO expression
                  | expression MOD expression
                  | expression SOMBRERITO expression
                  | PAREN_IZQ expression PAREN_DER
                  | number
                  | ID'''
    if len(p) > 2:
        if p[2] == "^":
            p[0] = "pow(" + p[1] + ", " + p[3] + ")"
        else:
            p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = p[1]


def p_fm_parameters(p):
    '''fm_parameters : WITH data_type ID COMA fm_parameters2
                     | empty'''
    if len(p) > 3:
        p[0] = p[2] + " " + p[3] + p[5]
    else:
        p[0] = ""


def p_fm_parameters2(p):
    '''fm_parameters2 : data_type ID COMA fm_parameters2
                      | empty'''
    if len(p) > 3:
        p[0] = p[3] + " " + p[1] + " " + p[2] + p[4]
    else:
        p[0] = ""


def p_cfm_arguments(p):
    '''cfm_arguments : WITH alguito cfm_arguments2
                     | empty'''
    if len(p) > 3:
        p[0] = p[2] + p[3]
    else:
        p[0] = ""


def p_cfm_arguments2(p):
    '''cfm_arguments2 : COMA alguito cfm_arguments2
                      | empty'''
    if len(p) > 3:
        p[0] = p[1] + " " + p[2] + p[3]
    else:
        p[0] = ""


def p_decrement(p):
    '''decrement : DECREMENT COMA
                 | empty'''
    if len(p) >= 3:
        p[0] = p[1]
    else:
        pass


def p_logic(p):
    '''logic : logic AND logic
             | logic OR logic
             | PAREN_IZQ logic PAREN_DER
             | NOT logic
             | condition'''
    if len(p) > 3:
        if p[2] == "AND":
            p[0] = p[1] + " && " + p[3]
        elif p[2] == "OR":
            p[0] = p[1] + " || " + p[3]
        else:
            p[0] = p[1] + p[2] + p[3]
    elif len(p) == 3:
        p[0] = "!" + p[2]
    else:
        p[0] = p[1]


def p_condition(p):
    '''condition : val MAYOR val
                 | val MENOR val
                 | val MAYOR_IGUAL val
                 | val MENOR_IGUAL val
                 | val DISTINTO val
                 | val IGUAL val
                 | val'''
    if len(p) >= 3:
        p[0] = p[1] + " " + p[2] + " " + p[3]
    else:
        p[0] = p[1]


def p_val(p):
    '''val : CADENA
           | read
           | distance
           | x_axis
           | y_axis
           | push
           | angle
           | boolean
           | number
           | ID'''
    p[0] = p[1]


# FUNCIONES AUXILIARES PARA TIPOS DE VARIABLES y DATOS


def p_data_type(p):
    '''data_type : STRING
                 | INT
                 | LONG
                 | BYTE
                 | CHAR
                 | FLOAT
                 | BOOLEAN'''
    if p[1] == "STRING":
        p[0] = "String"
    elif p[1] == "INT":
        p[0] = "int"
    elif p[1] == "LONG":
        p[0] = "long"
    elif p[1] == "BYTE":
        p[0] = "byte"
    elif p[1] == "CHAR":
        p[0] = "char"
    elif p[1] == "FLOAT":
        p[0] = "float"
    else:
        p[0] = "bool"


def p_value(p):
    '''value : HIGH
             | LOW'''
    p[0] = p[1]


def p_number(p):
    '''number : ENTERO
              | DECIMAL'''
    p[0] = p[1]


def p_boolean(p):
    '''boolean : TRUE
               | FALSE'''
    if p[1] == "TRUE":
        p[0] = "true"
    else:
        p[0] = "false"


# OTRAS FUNCIONES


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    global rosy_error
    rosy_error = True
    message = ""
    if p != None:
        message = "Error de sintaxis en la línea %s" % p.lineno
    else:
        message = "Unexpected end of input"

    showerror(title='Fallo al compilar', message=message)


'''---- DEFINICION DE PRECEDENCIA ----'''
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'ASTERISCO', 'BARRA'),
    ('left', 'MOD', 'SOMBRERITO'),
    ('left', 'AND', 'OR'),
    ('left', 'NOT'),
)


'''------- CREACION DE PARSER --------'''
parser = yacc.yacc()

'''-------- ----------------- --------'''


def compile(rosy_text, pini_text, name):
    global digital_variables
    global analog_variables

    global globals
    global functions_methods
    global rosy_error
    global distance_method
    global sounding_function
    global scoreboard_function
    global scoreboard_plus_function
    global number_function
    global text_function

    pini_result = pini_compile(pini_text)

    if pini_result is not None and pini_result != '':
        globals = ""
        functions_methods = "\n"
        rosy_error = False
        distance_method = True
        sounding_function = True
        scoreboard_function = True
        scoreboard_plus_function = True
        number_function = True
        text_function = True
        rosy_reset_lineno()

        result = parser.parse(rosy_text)

        if result is not None and not rosy_error:
            try:
                config = open(absolute + '/config.ini', 'r')
                folder = config.read()
                config.close()

                file_name = name[:name.find('.rosy')]
                path = folder[(folder.find('r=') + 2):].replace('\n', '') + '/' + file_name + '.ino'
                result = globals + pini_result + "\nvoid loop()\n{" + result + "}" + functions_methods

                file = open(path, 'w')
                file.write(result)
                file.close()

                showinfo(
                    title='Compilación exitosa',
                    message='Código fuente creado en la Carpeta de Archivos'
                )

            except:
                showerror(
                    title='Error',
                    message='Fallo al abrir la Carpeta de Archivos, revise su configuración en Archivo > Preferencias > Carpeta de Archivos.'
                )
                return
