# '''
#     main.py - GUI de Rosy IDE
#     Creado por M. Macoritto, Abril 2022.
#     Licencia Pública General de GNU (GPL) versión 3.
# '''

import re
import os
import platform
import webbrowser
import tkinter as tk
from tkinter import ttk, Menu, filedialog
from tkinter.messagebox import askyesno, showinfo, showerror
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

from utils import *
from pini_lex import reserved as pini_reserved
from rosy_lex import reserved as rosy_reserved
from rosy_yacc import compile

reserved_blue = [
    'HIGH',
    'LOW' ,
    'READ',
    'WRITE',
    'NO',
    'TONE',
    'PULSE',
    'DISTANCE',
    'X_AXIS',
    'Y_AXIS',
    'PUSH',
    'ANGLE',
    'ROTATE',
    'SOUNDING',
    'SCOREBOARD',
    'NUMBER',
    'DOT',
    'COLUMN',
    'ROW',
    'TEXT',
    'CLEAR',
    'pini'
]


def config_main_window(title, window_width, window_height):
    root.title(title)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.minsize(window_width, window_height)
    if platform.system() == 'Windows':
        root.iconbitmap(absolute + '/res/assets/logo.ico')
    root.columnconfigure(0, weight=100)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=10)
    root.columnconfigure(4, weight=1)
    root.columnconfigure(5, weight=1)
    root.columnconfigure(6, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=50)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3, weight=1)


def config_menu_bar():
    menubar = Menu(root)

    # File menu
    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label='Nuevo', command=lambda: new_file(rosy_text, rosy_file_path, rosy_file_name, rosy_extension))
    file_menu.add_command(label='Abrir...', command=open_rosy)
    file_menu.add_separator()
    file_menu.add_command(label='Compilar',
        command=lambda: compile(
            rosy_text.get('1.0', tk.END),
            pini_text.get('1.0', tk.END),
            rosy_file_name.get()
        )
    )
    file_menu.add_separator()
    file_menu.add_command(label='Guardar', command=lambda: save_file(rosy_file_path, rosy_text, rosy_extension))
    file_menu.add_command(label='Guardar Como...', command=lambda: save_file_as(rosy_extension, rosy_filetypes, rosy_file_name, rosy_text, rosy_file_path))
    file_menu.add_separator()
    # Preferences submenu
    sub_menu = Menu(file_menu, tearoff=0)
    sub_menu.add_command(label='Carpeta de Archivos...', command=set_folder)
    file_menu.add_cascade(label="Preferencias", menu=sub_menu)
    # Theme submenu
    sub_menu_theme = Menu(sub_menu, tearoff=0)
    sub_menu_theme.add_command(label='Claro', command=lambda: change_theme(1))
    sub_menu_theme.add_command(label='Oscuro', command=lambda: change_theme(0))
    sub_menu.add_cascade(label="Tema", menu=sub_menu_theme)

    file_menu.add_separator()
    file_menu.add_command(label='Salir', command=confirm_exit)
    menubar.add_cascade(label="Archivo", menu=file_menu, underline=0)

    # Edit menu
    edit_menu = Menu(menubar, tearoff=0)
    edit_menu.add_command(label='Deshacer', command=undo)
    edit_menu.add_command(label='Rehacer', command=redo)
    edit_menu.add_separator()
    edit_menu.add_command(label='Ir a...', command=goto_window)
    menubar.add_cascade(label="Editar", menu=edit_menu, underline=0)

    # Pini menu
    pini_menu = Menu(menubar, tearoff=0)
    pini_menu.add_command(label='Nueva Configuración', command=lambda: new_file(pini_text, pini_file_path, pini_file_name, pini_extension))
    pini_menu.add_command(label='Abrir...', command=open_pini)
    pini_menu.add_separator()
    pini_menu.add_command(label='Añadir Componente...', command=lambda: new_component_window(root, pini_text))
    pini_menu.add_separator()
    pini_menu.add_command(label='Guardar', command=lambda: save_file(pini_file_path, pini_text, pini_extension))
    pini_menu.add_command(label='Guardar Como...', command=lambda: save_file_as(pini_extension, pini_filetypes, pini_file_name, pini_text, pini_file_path))
    menubar.add_cascade(label="Pines", menu=pini_menu, underline=0)

    # Help menu
    help_menu = Menu(menubar, tearoff=0)
    help_menu.add_command(label='Ir a la Documentación...', command=lambda: webbrowser.open_new('https://rosy-ide.web.app/documentacion'))
    help_menu.add_command(label='Acerca de...', command=about_window)
    menubar.add_cascade(label="Ayuda", menu=help_menu, underline=0)

    return menubar


def demon(text, method_tag, method_count_line):
    text.bind('<KeyRelease>', method_tag)
    text.bind('<FocusIn>', method_tag)
    text.bind('<ButtonRelease>', method_count_line)
    text.bind('<KeyRelease-Down>', method_count_line)
    text.bind('<KeyRelease-Left>', method_count_line)
    text.bind('<KeyRelease-Right>', method_count_line)
    text.bind('<KeyRelease-Up>', method_count_line)
    text.bind('<KeyRelease-BackSpace>', method_count_line)
    text.bind('<KeyRelease-Delete>', method_count_line)
    text.bind('<KeyRelease-Insert>', method_count_line)
    text.bind('<KeyRelease-Return>', method_count_line)
    text.bind('<Control-KeyRelease-V>', method_count_line)
    text.bind('<Control-KeyRelease-v>', method_count_line)


def rosy_tags(event):
    text = rosy_text.get('1.0', tk.END)
    jockeys = [m.start() for m in re.finditer('\n', text)]
    for token in rosy_tokens:
        for position in [m.start() for m in re.finditer(token, text)]:
            line = text[:position].count('\n') + 1
            if line > 1:
                position -= (jockeys[line - 2] + 1)

            if token == cadena:
                linea = rosy_text.get(str(line) + '.' + str(position + 1), tk.END)
                cierre = linea.find('"')
                if cierre == -1:
                    cierre = linea.find("'")
                if cierre != -1:
                    rosy_text.tag_add(token + str(position), str(line) + '.' + str(position), str(line) + '.' + str(position + cierre + 2))
            else:
                rosy_text.tag_add(token + str(position), str(line) + '.' + str(position), str(line) + '.' + str(position + len(token)))

            color = naranja_oscuro
            if token == comment:
                color = gris
            elif token == cadena:
                color = verde
            elif token in reserved_blue:
                color = azul

            rosy_text.tag_config(token + str(position), foreground=color)


def pini_tags(event):
    text = pini_text.get('1.0', tk.END)
    jockeys = [m.start() for m in re.finditer('\n', text)]
    for token in pini_tokens:
        for position in [m.start() for m in re.finditer(token, text)]:
            line = text[:position].count('\n') + 1
            if line > 1:
                fase = jockeys[line - 2] + 1
                pini_text.tag_add(token + str(position), str(line) + '.' + str(position - fase), str(line) + '.' + str((position - fase) + len(token)))
            else:
                pini_text.tag_add(token + str(position), str(line) + '.' + str(position), str(line) + '.' + str(position + len(token)))

            color = naranja_oscuro
            if token == comment:
                color = gris

            pini_text.tag_config(token + str(position), foreground=color)


def rosy_count_line(event):
    rosy_line.set('Línea ' + str(rosy_text.get('1.0', tk.INSERT).count('\n') + 1))


def pini_count_line(event):
    pini_line.set('Pini: Línea ' + str(pini_text.get('1.0', tk.INSERT).count('\n') + 1))


def change_theme(theme):
    try:
        config = open(absolute + '/config.ini', 'r')
        old = config.read()
        config.close()

        config = open(absolute + '/config.ini', 'w')
        config.write('theme=' + str(theme) + old[old.find('\n'):])
        config.close()

        showinfo(
            title='Tema cambiado',
            message='Los cambios se aplicarán la próxima vez que abra el programa.'
        )

    except:
        showerror(title='Error', message=error_message_config)
        return


def set_folder():
    try:
        config = open(absolute + '/config.ini', 'r')
        data = config.read()
        config.close()

        path = data[(data.find('r=') + 2):].replace('\n', '')
        directory = filedialog.askdirectory(initialdir=path)

        if directory != () and directory != '':
            try:
                config = open(absolute + '/config.ini', 'w')
                config.write(data[:(data.find('r=') + 2)] + directory)
                config.close()

                showinfo(
                    title='Carpeta de Archivos cambiada',
                    message='Cuando compile un nuevo archivo, el código fuente se generará en la carpeta que acaba de seleccionar.'
                )

            except:
                showerror(title='Error', message=error_message_config)
                return

    except:
        showerror(title='Error', message=error_message_config)
        return


def check_config():
    try:
        config = open(absolute + '/config.ini', 'r')
        config.close()

    except:
        config = open(absolute + '/config.ini', 'w')
        config.write('theme=1\nfolder=' + absolute + '/ino')
        config.close()

        os.mkdir(absolute + '/ino')


def open_rosy():
    if rosy_text.get('1.0', tk.END) == '\n':
        open_file(rosy_filetypes, rosy_text, rosy_file_path, rosy_file_name)

    else:
        answer = askyesno(
            title='Advertencia',
            message=warning_message_open_file
        )
        if answer:
            open_file(rosy_filetypes, rosy_text, rosy_file_path, rosy_file_name)


def open_pini():
    if pini_text.get('1.0', tk.END) == '\n':
        open_file(pini_filetypes, pini_text, pini_file_path, pini_file_name)

    else:
        answer = askyesno(
            title='Advertencia',
            message=warning_message_open_file
        )
        if answer:
            open_file(pini_filetypes, pini_text, pini_file_path, pini_file_name)


def open_file(filetypes, text, path, name):
    filename = filedialog.askopenfilename(filetypes=filetypes)
    if filename != () and filename != '':
        try:
            position = len(filename) - filename[::-1].find('/')
            path.set(filename)
            name.set(filename[position:])

            file = open(filename, 'r')
            text.delete('1.0', tk.END)
            text.insert(tk.INSERT, file.read())
            file.close()

            text.focus()

        except:
            showerror(title='Error', message=error_message_open_file)
            return


def save_file(path, text, extension):
    if path.get() == '':
        if extension == rosy_extension:
            save_file_as(rosy_extension, rosy_filetypes, rosy_file_name, rosy_text, rosy_file_path)
        else:
            save_file_as(pini_extension, pini_filetypes, pini_file_name, pini_text, pini_file_path)

    else:
        try:
            file = open(path.get(), 'w')
            file.write(text.get('1.0', tk.END))
            file.close()

        except:
            showerror(title='Error', message=error_message_save_file)
            return


def save_file_as(extension, filetypes, name, text, path):
    filename = filedialog.asksaveasfilename(
        defaultextension=extension,
        initialfile=name.get(),
        filetypes=filetypes,
    )
    if filename != () and filename != '':
        try:
            file = open(filename, 'w')
            file.write(text.get('1.0', tk.END))
            file.close()

            position = len(filename) - filename[::-1].find('/')
            path.set(filename)
            name.set(filename[position:])

        except:
            showerror(title='Error', message=error_message_save_file)
            return


def new_file(text, path, name, extension):
    if text.get('1.0', tk.END) != '\n':
        answer = askyesno(
            title='Advertencia',
            message=warning_message_new_file
        )
        if answer:
            text.delete('1.0', tk.END)
            path.set('')
            name.set(default_name + extension)
            text.focus()


def confirm_exit():
    if rosy_text.get('1.0', tk.END) != '\n' or pini_text.get('1.0', tk.END) != '\n':
        answer = askyesno(
            title='Salir',
            message='¿Está seguro que desea salir? Se perderá todo el progreso no guardado.'
        )
        if answer:
            root.destroy()

    else:
        root.destroy()


def undo():
    try:
        rosy_text.edit_undo()
    except:
        return


def redo():
    try:
        rosy_text.edit_redo()
    except:
        return


def goto_window():
    linefind = tk.Tk()
    set_theme(linefind)
    config_inset_window(root, linefind, 'Ir a', 250, 100)
    linefind.columnconfigure(0, weight=1)
    linefind.columnconfigure(1, weight=1)
    linefind.rowconfigure(0, weight=1)
    linefind.rowconfigure(1, weight=1)
    line = tk.StringVar(linefind)
    ttk.Label(linefind, text='Ir a la línea').grid(column=0, row=0, sticky=tk.E, padx=2)
    entry = ttk.Entry(linefind, textvariable=line, width=10)
    entry.grid(column=1, row=0, sticky=tk.W, padx=2)
    entry.focus()
    ttk.Button(linefind, text='Cancelar', command=lambda: linefind.destroy()).grid(column=0, row=1, sticky=tk.W, padx=10)
    ttk.Button(linefind, text='Ir', command=lambda: goto_line(line, linefind)).grid(column=1, row=1, sticky=tk.E, padx=10)


def goto_line(line, main):
    main.destroy()
    try:
        rosy_text.mark_set(tk.INSERT, line.get() + '.0')
        rosy_text.see(tk.INSERT)
        rosy_count_line('event')
    except:
        showerror(title='Error', message='Línea inválida o inexistete.')
        return


def about_window():
    about = tk.Tk()
    set_theme(about)
    config_inset_window(root, about, 'Acerca de', 500, 300)
    about.columnconfigure(0, weight=2)
    about.columnconfigure(1, weight=1)
    about.columnconfigure(2, weight=100)
    about.rowconfigure(0, weight=2)
    about.rowconfigure(1, weight=1)
    about.rowconfigure(2, weight=1)
    about.rowconfigure(3, weight=2)
    logo_image = tk.PhotoImage(master=about, file=absolute + '/res/images/logo.png').subsample(3, 3)
    tk.Label(about, image=logo_image).grid(column=0, row=0, rowspan=4)
    tk.Label(about, text='Rosy IDE', font=('Times New Roman', 32, 'bold')).grid(column=1, row=0, columnspan=2, sticky=tk.SW, padx=5)
    tk.Label(about, text='Versión: 1.0', font=('Times New Roman', 16)).grid(column=1, row=1, columnspan=2, sticky=tk.NW, padx=5)
    tk.Label(about, text='Licencia:', font=('Times New Roman', 14)).grid(column=1, row=2, sticky=tk.NW, padx=5)

    licence = tk.Label(about, text='GNU GPLv3', font=('Times New Roman', 12, 'underline'), fg=azul, cursor='hand2')
    licence.grid(column=2, row=2, sticky=tk.NW, padx=5)
    licence.bind('<Button-1>', lambda e: webbrowser.open_new('https://www.gnu.org/licenses/gpl-3.0.txt'))

    link = tk.Label(about, text='Ir al sitio web', font=('Arial', 12, 'underline'), fg=azul, cursor='hand2')
    link.grid(column=1, row=3, columnspan=2, sticky=tk.NW, padx=5)
    link.bind('<Button-1>', lambda e: webbrowser.open_new('https://rosy-ide.web.app'))

    about.mainloop()


root = tk.Tk()
check_config()
set_theme(root)
config_main_window('Rosy IDE', 1000, 600)

save_icon = tk.PhotoImage(file=absolute + '/res/images/save.png')
compile_icon = tk.PhotoImage(file=absolute + '/res/images/compile.png')
open_icon = tk.PhotoImage(file=absolute + '/res/images/open.png')
add_icon = tk.PhotoImage(file=absolute + '/res/images/add.png')

comment = r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
cadena = r'[\"][^"\n]*[\"]|[\'][^\'\n]*[\']'
default_name = 'sin-titulo'
rosy_extension = '.rosy'
pini_extension = '.pini'
rosy_filetypes = [('Rosy', '*' + rosy_extension)]
pini_filetypes = [('Configuración de pines', '*' + pini_extension)]

rosy_tokens = list(rosy_reserved.values())
rosy_tokens.append(comment)
rosy_tokens.append(cadena)
pini_tokens = list(pini_reserved.values())
pini_tokens.append(comment)

rosy_file_path = tk.StringVar()
pini_file_path = tk.StringVar()
rosy_file_name = tk.StringVar()
pini_file_name = tk.StringVar()
rosy_line = tk.StringVar()
pini_line = tk.StringVar()

rosy_file_path.set('')
pini_file_path.set('')
rosy_file_name.set(default_name + rosy_extension)
pini_file_name.set(default_name + pini_extension)
rosy_line.set('Línea 1')
pini_line.set('Pini: Línea 1')

# Arduino UNO image
arduino_uno = tk.PhotoImage(file=absolute + '/res/images/UNO.png').subsample(2, 2)
tk.Label(root, image=arduino_uno).grid(column=3, columnspan=4, row=2, pady=5)

# Line counter
tk.Label(root, textvariable=rosy_line).grid(column=0, columnspan=2, row=3, sticky=tk.W, padx=3)
tk.Label(root, textvariable=pini_line).grid(column=3, columnspan=4, row=3, sticky=tk.E, padx=10, pady=(0, 5))

'''---- ROSY -----'''
# Text editor area
rosy_text = ScrolledText(root, width=50, height=10, undo=True)
rosy_text.grid(column=0, columnspan=3, row=1, rowspan=2, sticky=tk.NSEW, padx=(3, 0))
demon(rosy_text, rosy_tags, rosy_count_line)

# Actions
tk.Label(root, textvariable=rosy_file_name).grid(column=0, row=0, sticky=tk.W, padx=5, pady=(3, 0))
ttk.Button(root, image=save_icon, command=lambda: save_file(rosy_file_path, rosy_text, rosy_extension)).grid(column=1, row=0, pady=3)
ttk.Button(root, image=compile_icon,
    command=lambda: compile(
        rosy_text.get('1.0', tk.END),
        pini_text.get('1.0', tk.END),
        rosy_file_name.get()
    )
).grid(column=2, row=0, pady=3)

'''---- PINI -----'''
# Text editor area
pini_text = ScrolledText(root, width=50, height=10, undo=True)
pini_text.grid(column=3, columnspan=4, row=1, sticky=tk.NSEW, padx=5, pady=(0, 3))
demon(pini_text, pini_tags, pini_count_line)

# Actions
tk.Label(root, textvariable=pini_file_name).grid(column=3, row=0, sticky=tk.W, padx=5, pady=(3, 0))
ttk.Button(root, image=open_icon, command=open_pini).grid(column=4, row=0, pady=3)
ttk.Button(root, image=save_icon, command=lambda: save_file(pini_file_path, pini_text, pini_extension)).grid(column=5, row=0, pady=3)
ttk.Button(root, image=add_icon, command=lambda: new_component_window(root, pini_text)).grid(column=6, row=0, pady=3)

'''---- MAIN -----'''
root.protocol("WM_DELETE_WINDOW", confirm_exit)
menubar = config_menu_bar()
root.config(menu=menubar)
root.mainloop()
