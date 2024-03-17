# Modulos importados
from tkinter import *
from tkinter import ttk
import tkinter as tk
import time
from tkinter.messagebox import *
from modelo import FuncionesBotonera

class VistaPrincipal(Frame):
    """
    - Clase VistaPrincipal: que representa la interfaz principal de la aplicación."""

    def __init__(self, window):
        """
        - Inicializa la ventana principal.
        
        :param window: La ventana principal de la aplicación.
        """
        super().__init__(window)
        self.root = window
        self.root.title("Registro De Clientes - Estudio Contable 🏛️ ")
        self.root.configure(bg="#3157FF")
        self.objeto_botones = FuncionesBotonera()
        self.crear_interfaz()

        style = ttk.Style()
        style.configure('Treeview', background='#D6ECFA', foreground='black', font=('Arial', 10, 'bold'))

        # Agregar reloj en la parte inferior con grid
        self.clock = Clock(self.root)
        self.clock.grid(row=500, column=0, columnspan=7, sticky="we")

    def crear_interfaz(self):
        """
        - Funcion para mi interfaz: Crea la interfaz gráfica de la ventana principal.

        - Crea un título con el texto "Plantilla de clientes - Ingrese sus datos" y lo coloca en la parte superior de la ventana.
        - Define cinco variables de control (`StringVar`) para los campos de entrada de texto.
        - Crea cinco campos de entrada de texto para que el usuario ingrese datos:
          - Nombre
          - Apellido
          - Rubro/Oficio
          - CUIT/CUIL
          - Clave Fiscal
        """
        row_offset = 1

         #titulo de la aplicacion
        self.titulo = Label(self.root, text="Plantilla de clientes - Ingrese sus datos", font=("Arial", 16, "bold"), fg="black", bg="white")
        self.titulo.grid(row=0, column=0, columnspan=6, pady=(10, 10), sticky="we")

        # Variables de control
        self.a_val = StringVar()
        self.b_val = StringVar()
        self.c_val = StringVar()
        self.d_val = StringVar()
        self.e_val = StringVar()

        self.entrada1 = self.crear_fila_entrada("Nombre", self.a_val, width=30)
        self.entrada2 = self.crear_fila_entrada("Apellido", self.b_val, width=30)
        self.entrada3 = self.crear_fila_entrada("Rubro/Oficio", self.c_val, width=30)
        self.entrada4 = self.crear_fila_entrada("CUIT/CUIL", self.d_val, width=30)
        self.entrada5 = self.crear_fila_entrada_contrasena("Clave Fiscal", self.e_val, width=30)

        # Agregar reloj en la parte inferior con grid
        self.clock = Clock(self.root)
        self.clock.grid(row=500, column=0, columnspan=7, sticky="we")

    def crear_fila_entrada(self, nombre, textvariable, width):
        """
        - Funcion para edicion de la entrada de datos: Crea una fila de entrada de texto.

        :param nombre: El nombre del campo.
        :param textvariable: La variable de control asociada al campo.
        :param width: El ancho del campo en caracteres.
        """
        frame = Frame(self.root, bg="white")
        frame.grid()
        label = Label(frame, text=nombre, bg="black", fg="white", width=20)
        label.grid(row=3, column=0, sticky=W)
        entry = Entry(frame, textvariable=textvariable, width=width)
        entry.grid(row=3, column=1, sticky=W)
        return frame

    def crear_fila_entrada_contrasena(self, nombre, textvariable, width, show_char='*'):
        """
        - Funcion para edicion de la entrada de contraseña: Crea una fila de entrada de texto con opción para contraseña.
        :param nombre: El nombre del campo.
        :param textvariable: La variable de control asociada al campo.
        :param width: El ancho del campo en caracteres.
        :param show_char: El carácter a mostrar en lugar del texto.
        """
        frame = Frame(self.root, bg="white")
        frame.grid()
        label = Label(frame, text=nombre, bg="black", fg="white", width=20)
        label.grid(row=4, column=0, sticky=W)
        entry = Entry(frame, textvariable=textvariable, width=width, show=show_char)
        entry.grid(row=4, column=4, sticky=W, padx=(0, 5))

        # Opcion de veo o no ver la clave fiscal
        show_password_var = BooleanVar()
        show_password_checkbox = Checkbutton(text="Mostrar contraseña", variable=show_password_var, command=lambda:self.objeto_botones.toggle_password(show_password_var, entry, show_char))
        show_password_checkbox.grid(row=5, column=1, sticky=W, padx=(5, 0))

    #TREEVIEWS
    def crear_treeview(self):
        """
        - Funcion TREVIEW: Crea y configura un widget Treeview."""
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5")
        self.tree.column("#0", width=40, minwidth=40, anchor=W)

        for col in ("col1", "col2", "col3", "col4", "col5"):
            self.tree.column(col, width=150, minwidth=150, anchor=W)
        
        self.tree.column("col1", width=150, minwidth=150, anchor=W)
        self.tree.column("col2", width=150, minwidth=150, anchor=W)
        self.tree.column("col3", width=150, minwidth=150, anchor=W)
        self.tree.column("col4", width=150, minwidth=150, anchor=W)
        self.tree.column("col5", width=150, minwidth=150, anchor=W)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Nombre")
        self.tree.heading("col2", text="Apellido")
        self.tree.heading("col3", text="Rubro / Oficio")
        self.tree.heading("col4", text="CUIT / CUIL")
        self.tree.heading("col5", text="Clave Fiscal")
        self.tree.grid(row=row_offset + 5, column=0, columnspan=6, pady=(10, 10))
    
    #BOTONERA
        
class Botones():
    """- Clase que gestiona los botones de la interfaz."""

    def __init__(self, root, objeto_botones, a_val, b_val, c_val, d_val, e_val, tree):
        """
        - Inicializa la botonera.

        :param root: El widget raíz de la aplicación.
        :param objeto_botones: Objeto que contiene las funciones de la botonera.
        :param a_val: Variable de control para el campo "Nombre".
        :param b_val: Variable de control para el campo "Apellido".
        :param c_val: Variable de control para el campo "Rubro/Oficio".
        :param d_val: Variable de control para el campo "CUIT/CUIL".
        :param e_val: Variable de control para el campo "Clave Fiscal".
        :param tree: Widget Treeview donde se muestran los datos.
        """
        self.root = root
        self.objeto_botones = objeto_botones
        self.a_val = a_val
        self.b_val = b_val
        self.c_val = c_val
        self.d_val = d_val
        self.e_val = e_val
        self.tree = tree
        self.crear_botones()

    def crear_botones(self):
        """- Funcion para crear botones: Crea los botones de la interfaz y los configura con las funciones correspondientes."""
        row_offset = 1

        # Botón para agregar cliente
        self.boton_alta = self.crear_boton("Agregar Cliente", lambda:self.objeto_botones.alta(self.a_val, self.b_val, self.c_val, self.d_val, self.e_val, self.tree))
        self.boton_alta.grid(row=row_offset + 6, column=0, padx=(0, 10), pady=10)

        # Botón para modificar cliente
        self.boton_modificar = self.crear_boton("Modificar Cliente", lambda:self.objeto_botones.modificar(self.tree, self.a_val, self.b_val, self.c_val, self.d_val, self.e_val))
        self.boton_modificar.grid(row=row_offset + 6, column=2, padx=(0, 10), pady=10)

        # Botón para eliminar cliente
        self.boton_borrar = self.crear_boton("Eliminar Cliente", lambda:self.objeto_botones.borrar(self.tree))
        self.boton_borrar.grid(row=row_offset + 6, column=3, padx=(0, 10), pady=10)

        # Botón para consultar cliente
        self.boton_consulta = self.crear_boton("Consultar Cliente", lambda:self.objeto_botones.consultar(self.tree, self.a_val, self.b_val, self.c_val, self.d_val, self.e_val))
        self.boton_consulta.grid(row=row_offset + 6, column=1, padx=(0, 10), pady=10)

    def crear_boton(self, text, command=None, **kwargs):
        """
        - Funcion para definir botones: Crea un botón con el texto especificado y la función de comando indicada.

        :param text: El texto del botón.
        :param command: La función de comando que se ejecuta al hacer clic en el botón.
        """
        default_kwargs = dict(bg="black", fg="white", font=('Arial', 10, 'bold'))
        default_kwargs.update(kwargs)
        return Button(self.root, text=text, command=command, **default_kwargs)

    # Reloj inferior con fecha
class Clock(tk.Label):
    """- Funcion para reloj y fecha: Clase que muestra un reloj con la fecha actual."""

    def __init__(self, parent):
        """
        Inicializa el reloj.

        :param parent: El widget padre del reloj.
        """
        tk.Label.__init__(self, parent, font=('Arial', 12, 'bold'))
        self.parent = parent
        self.time_string = tk.StringVar()
        self.time_string.set(self.get_current_time())
        self.configure(textvariable=self.time_string)

        self.update_clock()

    def get_current_time(self):
        """- Funcion formato: Obtiene la fecha y hora actual en formato 'dd/mm/yyyy - hh:mm:ss'."""
        return time.strftime('%d/%m/%Y  -  %H:%M:%S')

    def update_clock(self):
        """- Funcion de actulizacion: Actualiza el reloj con la fecha y hora actuales."""
        self.time_string.set(self.get_current_time())
        self.after(1000, self.update_clock)
