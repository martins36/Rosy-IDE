# '''
#     utils.py - Utilidades para la GUI de Rosy IDE
#     Creado por M. Macoritto, Abril 2022.
#     Licencia Pública General de GNU (GPL) versión 3.
# '''

import os
import platform
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from PIL import Image, ImageTk

absolute = os.path.dirname(os.path.realpath(__file__))

error_message_config = 'Fallo al abrir config.ini, revise que el archivo exista.'
error_message_open_file='Fallo al abrir el archivo seleccionado.'
error_message_save_file='Fallo al guardar el archivo.'
warning_message_open_file='¿Está seguro que desea abrir otro archivo? Se perderá el progreso no guardado.'
warning_message_new_file='¿Está seguro que desea crear un nuevo archivo? Se perderá el progreso no guardado.'

digitales = ('2', '3', '4', '5', '6', '7', '8','9', '10', '11', '12', '13')
analogicos = ('A0', 'A1', 'A2', 'A3', 'A4', 'A5')
pwm = ('3', '5', '6', '9', '10', '11')

naranja_oscuro = '#ff6d00'
naranja = '#ffab00'
verde = '#00c853'
azul = "#2962ff"
gris = "#9e9e9e"


def set_theme(root):
    try:
        config = open(absolute + '/config.ini', 'r')
        line = config.read()
        config.close()

        if line[6:7] == '1':
            root.tk.call('source', absolute + '/res/themes/azure/azure.tcl')
        else:
            root.tk.call('source', absolute + '/res/themes/azure dark/azure dark.tcl')

        style = ttk.Style(root)
        style.theme_use('azure')

    except:
        showerror(
            title='Error',
            message=error_message_config
        )
        return


def config_inset_window(root, container, title, window_width, window_height):
    container.title(title)
    screen_x = root.winfo_rootx()
    root_width = root.winfo_width()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_x + ( root_width / 2) - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    container.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    container.resizable(False, False)
    if platform.system() == 'Windows':
        container.iconbitmap(absolute + '/res/assets/logo.ico')


def new_component_window(root, pini_text):
    select_component = tk.Tk()
    set_theme(select_component)
    config_inset_window(root, select_component, 'Seleccione un Componente', 900, 700)

    global naranja
    global naranja_oscuro
    global verde
    global digitales
    global analogicos
    global pwm

    output = ', OUT'
    input_pullup = ', INP_PUL'
    pin = 'PIN '

    button_text = 'Botón'
    buzzer_text = 'Buzzer'
    cny70_text = 'CNY70'
    display4d_text = 'Módulo Display 4 Dígitos'
    joystick_text = 'Módulo Joystick'
    ldr_text = 'LDR'
    led_text = 'LED'
    lm35_text = 'LM35'
    matrix_text = 'Módulo Matriz LED 8x8'
    puenteh_text = 'Puente H'
    servo_text = 'Servomotor SG90'
    ultra_text = 'Sensor Ultrasónico'

    button_img = absolute + '/res/images/button.png'
    buzzer_img = absolute + '/res/images/buzzer.png'
    cny70_img = absolute + '/res/images/cny70.png'
    display4d_img = absolute + '/res/images/display4d.png'
    joystick_img = absolute + '/res/images/joystick.png'
    ldr_img = absolute + '/res/images/ldr.png'
    led_img = absolute + '/res/images/led.png'
    lm35_img = absolute + '/res/images/lm35.png'
    matrix_img = absolute + '/res/images/matrix.png'
    puenteh_img = absolute + '/res/images/puenteh.png'
    servo_img = absolute + '/res/images/servo.png'
    ultra_img = absolute + '/res/images/ultra.png'

    button = tk.PhotoImage(master=select_component, file=button_img).subsample(2, 2)
    buzzer = tk.PhotoImage(master=select_component, file=buzzer_img).subsample(2, 2)
    cny70 = tk.PhotoImage(master=select_component, file=cny70_img).subsample(2, 2)
    display4d = tk.PhotoImage(master=select_component, file=display4d_img).subsample(2, 2)
    joystick = tk.PhotoImage(master=select_component, file=joystick_img).subsample(2, 2)
    ldr = tk.PhotoImage(master=select_component, file=ldr_img).subsample(2, 2)
    led = tk.PhotoImage(master=select_component, file=led_img).subsample(2, 2)
    lm35 = tk.PhotoImage(master=select_component, file=lm35_img).subsample(2, 2)
    matrix = tk.PhotoImage(master=select_component, file=matrix_img).subsample(2, 2)
    puenteh = tk.PhotoImage(master=select_component, file=puenteh_img).subsample(2, 2)
    servo = tk.PhotoImage(master=select_component, file=servo_img).subsample(2, 2)
    ultra = tk.PhotoImage(master=select_component, file=ultra_img).subsample(2, 2)

    select_component.columnconfigure(0, weight=1)
    select_component.columnconfigure(1, weight=1)
    select_component.columnconfigure(2, weight=1)
    select_component.columnconfigure(3, weight=1)
    select_component.columnconfigure(4, weight=1)
    select_component.columnconfigure(5, weight=1)
    select_component.rowconfigure(0, weight=1)
    select_component.rowconfigure(1, weight=1)
    select_component.rowconfigure(2, weight=1)

    ttk.Button( # Botón
        select_component,
        image=button, text=button_text, compound=tk.TOP,
        command=lambda: component_onepin_window(root, select_component, 250, 225,
            button_text, 'boton', digitales, pin, input_pullup, naranja, button_img, pini_text
        )
    ).grid(column=0, row=0)

    ttk.Button( # CNY70
        select_component,
        image=cny70, text=cny70_text, compound=tk.TOP,
        command=lambda: component_onepin_window(root, select_component, 250, 275,
            cny70_text, 'cny', analogicos, pin, '', verde, cny70_img, pini_text
        )
    ).grid(column=1, row=0)

    ttk.Button( # LM35
        select_component,
        image=lm35, text=lm35_text, compound=tk.TOP,
        command=lambda: component_onepin_window(root, select_component, 250, 300,
            lm35_text, 'lm35', analogicos, pin, '', verde, lm35_img, pini_text
        )
    ).grid(column=2, row=0)

    ttk.Button( # LDR
        select_component,
        image=ldr, text=ldr_text, compound=tk.TOP,
        command=lambda: component_onepin_window(root, select_component, 250, 300,
            ldr_text, 'ldr', analogicos, pin, '', verde, ldr_img, pini_text
        )
    ).grid(column=3, row=0)

    ttk.Button( #LED
        select_component,
        image=led, text=led_text, compound=tk.TOP,
        command=lambda: component_onepin_window(root, select_component, 250, 350,
            led_text, 'led', digitales, pin, output, naranja, led_img, pini_text
        )
    ).grid(column=4, row=0)

    ttk.Button( # Buzzer
        select_component,
        image=buzzer, text=buzzer_text, compound=tk.TOP,
        command=lambda: component_onepin_window(root, select_component, 300, 450,
            buzzer_text, 'buzzer', digitales, pin, output, naranja, buzzer_img, pini_text
        )
    ).grid(column=5, row=0)

    ttk.Button( # Servomotor SG90
        select_component,
        image=servo, text=servo_text, compound=tk.TOP,
        command=lambda: component_onepin_window(root, select_component, 550, 350,
            servo_text, 'servo', pwm, 'SERVO ', '', naranja_oscuro, servo_img, pini_text
        )
    ).grid(column=0, columnspan=2, row=1)

    ttk.Button( # Sensor Ultrasónico
        select_component,
        image=ultra, text=ultra_text, compound=tk.TOP,
        command=lambda: component_twopin_window(root, select_component, 500, 450,
            ultra_text, 'ultra', 'ULTRASONIC ', 'Trig', 'Echo', ultra_img, pini_text
        )
    ).grid(column=2, columnspan=2, row=1)

    ttk.Button( # Puente H
        select_component,
        image=puenteh, text=puenteh_text, compound=tk.TOP,
        command=lambda: component_fourpin_window(root, select_component, 800, 600,
            puenteh_text, 'puente', pin, output, puenteh_img, pini_text
        )
    ).grid(column=4, columnspan=2, row=1)

    ttk.Button( # Módulo Display 4 Dígitos
        select_component,
        image=display4d, text=display4d_text, compound=tk.TOP,
        command=lambda: component_twopin_window(root, select_component, 450, 350,
            display4d_text, 'display4d', 'DISPLAY ', 'CLK', 'DIO', display4d_img, pini_text
        )
    ).grid(column=0, columnspan=2, row=2)

    ttk.Button( # Módulo Joystick'
        select_component,
        image=joystick, text=joystick_text, compound=tk.TOP,
        command=lambda: component_threepin_window(root, select_component, 600, 400,
            joystick_text, 'joystick', 'JOYSTICK ', 'VRx', analogicos, verde,
            'VRy', 'SW', joystick_img, pini_text
        )
    ).grid(column=2, columnspan=2, row=2)

    ttk.Button( # Módulo Matriz LED 8x8
        select_component,
        image=matrix, text=matrix_text, compound=tk.TOP,
        command=lambda: component_threepin_window(root, select_component, 850, 500,
            matrix_text, 'matriz', 'MATRIX 1, ', 'DIN', digitales, naranja,
            'CLK', 'CS', matrix_img, pini_text
        )
    ).grid(column=4, columnspan=2, row=2)

    select_component.mainloop()


def component_onepin_window(root, container, window_width, window_height, title, nombre, pin_type, pin, io, color, img, pini_text):
    container.destroy()
    component = tk.Tk()
    set_theme(component)
    config_inset_window(root, component, title, window_width, window_height)
    component.columnconfigure(0, weight=1)
    component.columnconfigure(1, weight=1)
    component.rowconfigure(0, weight=1)
    component.rowconfigure(1, weight=1)
    component.rowconfigure(2, weight=1)
    component.rowconfigure(3, weight=1)

    id = tk.StringVar(component, nombre)
    option_var = tk.StringVar(component)
    image = tk.PhotoImage(master=component, file=img)

    ttk.Label(
        component,
        image=image
    ).grid(column=0, columnspan=2, row=0)

    ttk.Label(
        component,
        text='Nombre'
    ).grid(column=0, row=1, sticky=tk.E, padx=2)

    entry = ttk.Entry(component, textvariable=id, width=12)
    entry.grid(column=1, row=1, sticky=tk.W, padx=2)
    entry.focus()
    entry.icursor(len(nombre))

    tk.Label(
        component,
        text='PIN',
        bg=color
    ).grid(column=0, row=2, sticky=tk.E, padx=2)

    ttk.OptionMenu(
        component,
        option_var, pin_type[0],
        *pin_type
    ).grid(column=1, row=2, sticky=tk.W, padx=2)

    ttk.Button(
        component,
        text='Cancelar',
        command=lambda: component.destroy()
    ).grid(column=0, row=3, sticky=tk.W, padx=10)

    ttk.Button(
        component,
        text='Agregar',
        command=lambda: add_component(
            component, pini_text,
            pin + option_var.get() + ', ' + id.get().replace(' ', '') + io +
            ' /*' + title + '*/\n'
        )
    ).grid(column=1, row=3, sticky=tk.E, padx=10)

    component.mainloop()


def component_twopin_window(root, container, window_width, window_height, title, nombre, type, pin1, pin2, img, pini_text):
    container.destroy()
    component = tk.Tk()
    set_theme(component)
    config_inset_window(root, component, title, window_width, window_height)
    component.columnconfigure(0, weight=3)
    component.columnconfigure(1, weight=1)
    component.columnconfigure(2, weight=1)
    component.columnconfigure(3, weight=3)
    component.rowconfigure(0, weight=1)
    component.rowconfigure(1, weight=1)
    component.rowconfigure(2, weight=1)
    component.rowconfigure(3, weight=1)

    global naranja
    global digitales

    id = tk.StringVar(component, nombre)
    option_var1 = tk.StringVar(component)
    option_var2 = tk.StringVar(component)
    image = tk.PhotoImage(master=component, file=img)

    ttk.Label(
        component,
        image=image
    ).grid(column=0, columnspan=4, row=0)

    ttk.Label(
        component,
        text='Nombre'
    ).grid(column=0, row=1, columnspan=2, sticky=tk.E, padx=2)

    entry = ttk.Entry(component, textvariable=id, width=14)
    entry.grid(column=2, row=1, columnspan=2, sticky=tk.W, padx=2)
    entry.focus()
    entry.icursor(len(nombre))

    tk.Label(
        component,
        text=pin1,
        bg=naranja
    ).grid(column=0, row=2, sticky=tk.E, padx=2)

    ttk.OptionMenu(
        component,
        option_var1, digitales[0],
        *digitales
    ).grid(column=1, row=2, sticky=tk.W, padx=2)

    tk.Label(
        component,
        text=pin2,
        bg=naranja
    ).grid(column=2, row=2, sticky=tk.E, padx=2)

    ttk.OptionMenu(
        component,
        option_var2, digitales[2],
        *digitales
    ).grid(column=3, row=2, sticky=tk.W, padx=2)

    ttk.Button(
        component,
        text='Cancelar',
        command=lambda: component.destroy()
    ).grid(column=0, row=3, sticky=tk.W, padx=10)

    ttk.Button(
        component,
        text='Agregar',
        command=lambda: add_component(
            component, pini_text,
            type + option_var1.get() + ', ' + option_var2.get() + ', ' + id.get().replace(' ', '')
            + ' /*' + title + '*/\n'
        )
    ).grid(column=3, row=3, sticky=tk.E, padx=10)

    component.mainloop()


def component_threepin_window(root, container, window_width, window_height, title, nombre, type, pin1, pin1_type, pin1_color, pin2, pin3, img, pini_text):
    container.destroy()
    component = tk.Tk()
    set_theme(component)
    config_inset_window(root, component, title, window_width, window_height)
    component.columnconfigure(0, weight=1)
    component.columnconfigure(1, weight=1)
    component.columnconfigure(2, weight=1)
    component.rowconfigure(0, weight=1)
    component.rowconfigure(1, weight=1)
    component.rowconfigure(2, weight=1)
    component.rowconfigure(3, weight=1)
    component.rowconfigure(4, weight=1)

    global naranja
    global digitales

    id = tk.StringVar(component, nombre)
    option_var1 = tk.StringVar(component)
    option_var2 = tk.StringVar(component)
    option_var3 = tk.StringVar(component)
    image = tk.PhotoImage(master=component, file=img)

    ttk.Label(
        component,
        image=image
    ).grid(column=2, row=0, rowspan=3)

    ttk.Label(
        component,
        text='Nombre'
    ).grid(column=0, columnspan=2, row=3, sticky=tk.E, padx=2)

    entry = ttk.Entry(component, textvariable=id)
    entry.grid(column=2, row=3, sticky=tk.W, padx=2)
    entry.focus()
    entry.icursor(len(nombre))

    tk.Label(
        component,
        text=pin1,
        bg=pin1_color
    ).grid(column=0, row=0, sticky=tk.SE, padx=2)

    ttk.OptionMenu(
        component,
        option_var1, pin1_type[0],
        *pin1_type
    ).grid(column=1, row=0, sticky=tk.SW, padx=2)

    tk.Label(
        component,
        text=pin2,
        bg=pin1_color
    ).grid(column=0, row=1, sticky=tk.E, padx=2)

    ttk.OptionMenu(
        component,
        option_var2, pin1_type[2],
        *pin1_type
    ).grid(column=1, row=1, sticky=tk.W, padx=2)

    tk.Label(
        component,
        text=pin3,
        bg=naranja
    ).grid(column=0, row=2, sticky=tk.NE, padx=2)

    ttk.OptionMenu(
        component,
        option_var3, digitales[5],
        *digitales
    ).grid(column=1, row=2, sticky=tk.NW, padx=2)

    ttk.Button(
        component,
        text='Cancelar',
        command=lambda: component.destroy()
    ).grid(column=0, row=4, sticky=tk.W, padx=10)

    ttk.Button(
        component,
        text='Agregar',
        command=lambda: add_component(
            component, pini_text,
            type + option_var1.get() + ', ' + option_var2.get() + ', ' + option_var3.get()
            + ', ' + id.get().replace(' ', '') + ' /*' + title + '*/\n'
        )
    ).grid(column=2, row=4, sticky=tk.E, padx=10)

    component.mainloop()


def component_fourpin_window(root, container, window_width, window_height, title, nombre, pin, output, img, pini_text):
    container.destroy()
    component = tk.Tk()
    set_theme(component)
    config_inset_window(root, component, title, window_width, window_height)
    component.columnconfigure(0, weight=1)
    component.columnconfigure(1, weight=1)
    component.columnconfigure(2, weight=1)
    component.columnconfigure(3, weight=1)
    component.columnconfigure(4, weight=1)
    component.columnconfigure(5, weight=1)
    component.rowconfigure(0, weight=1)
    component.rowconfigure(1, weight=1)
    component.rowconfigure(2, weight=1)
    component.rowconfigure(3, weight=1)

    global naranja_oscuro
    global pwm

    id = tk.StringVar(component, nombre)
    option_var1 = tk.StringVar(component)
    option_var2 = tk.StringVar(component)
    option_var3 = tk.StringVar(component)
    option_var4 = tk.StringVar(component)
    image = tk.PhotoImage(master=component, file=img)

    ttk.Label(
        component,
        image=image
    ).grid(column=2, columnspan=2 , row=0, rowspan=2)

    ttk.Label(
        component,
        text='Nombre'
    ).grid(column=0, columnspan=3, row=2, sticky=tk.E, padx=2)

    entry = ttk.Entry(component, textvariable=id)
    entry.grid(column=3, columnspan=3, row=2, sticky=tk.W, padx=2)
    entry.focus()
    entry.icursor(len(nombre))

    tk.Label(
        component,
        text='IN1',
        bg=naranja_oscuro
    ).grid(column=0, row=0, sticky=tk.SE, padx=2)

    ttk.OptionMenu(
        component,
        option_var1, pwm[0],
        *pwm
    ).grid(column=1, row=0, sticky=tk.SW, padx=2)

    tk.Label(
        component,
        text='IN2',
        bg=naranja_oscuro
    ).grid(column=0, row=1, sticky=tk.E, padx=2)

    ttk.OptionMenu(
        component,
        option_var2, pwm[1],
        *pwm
    ).grid(column=1, row=1, sticky=tk.W, padx=2)

    tk.Label(
        component,
        text='IN4',
        bg=naranja_oscuro
    ).grid(column=4, row=0, sticky=tk.SE, padx=2)

    ttk.OptionMenu(
        component,
        option_var4, pwm[3],
        *pwm
    ).grid(column=5, row=0, sticky=tk.SW, padx=2)

    tk.Label(
        component,
        text='IN3',
        bg=naranja_oscuro
    ).grid(column=4, row=1, sticky=tk.E, padx=2)

    ttk.OptionMenu(
        component,
        option_var3, pwm[2],
        *pwm
    ).grid(column=5, row=1, sticky=tk.W, padx=2)

    ttk.Button(
        component,
        text='Cancelar',
        command=lambda: component.destroy()
    ).grid(column=0, row=3, sticky=tk.W, padx=10)

    ttk.Button(
        component,
        text='Agregar',
        command=lambda: add_component(
            component, pini_text,
            pin + option_var1.get() + ', ' + id.get().replace(' ', '') + '_in1' + output
            + ' /*' + title + ' IN1*/\n' +
            pin + option_var2.get() + ', ' + id.get().replace(' ', '') + '_in2' + output
            + ' /*' + title + ' IN2*/\n' +
            pin + option_var3.get() + ', ' + id.get().replace(' ', '') + '_in3' + output
            + ' /*' + title + ' IN3*/\n' +
            pin + option_var4.get() + ', ' + id.get().replace(' ', '') + '_in4' + output
            + ' /*' + title + ' IN4*/\n'
        )
    ).grid(column=5, row=3, sticky=tk.E, padx=10)

    component.mainloop()


def add_component(container, pini_text, line):
    pini_text.insert(tk.END, line)
    pini_text.focus()
    container.destroy()
