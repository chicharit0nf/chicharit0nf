# Modulos importados
from tkinter import *
from tkinter.messagebox import *
from peewee import *
import webbrowser
import datetime

midb = SqliteDatabase("base_clientes.db")

class BaseModel(Model):

    class Meta():
        """
        :param database: creamos con nombre nuestra base de datos. """
        database = midb

class Clientes(BaseModel):
    """- Clase que representa la tabla 'Clientes' en la base de datos.
    
    defininimos entonces...

    :param nombre: Nombre del cliente.

    :param apellido: Apellido del cliente.

    :param rubro: Rubro u oficio del cliente.

    :param cuit: CUIT/CUIL del cliente.

    :param clave_fiscal: Clave fiscal del cliente.


    """
    nombre = CharField()
    apellido = CharField()
    rubro = CharField()
    cuit = IntegerField()
    clave_fiscal = CharField()

midb.connect()
midb.create_tables([Clientes])

class ManejoErrores():

    @staticmethod
    def registrar_error(mensaje):
        """- Funcion registro de error: Registra un error en el archivo 'errores.txt' y muestra un mensaje de error.
        
        :param mensaje: El mensaje de error a registrar.
        
        :type mensaje: str
        
        """
        error = f"Se ha dado un error, {mensaje}"
        with open("errores.txt", "a") as log:
            log.write(f"{datetime.datetime.now()}: {error}\n")
        showerror("Error", error)

    @staticmethod
    def registrar_movimiento(mensaje):
        """- Funcion registro de accion: Registra una operación del usuario en el archivo 'root.txt'.
        
        :param mensaje: El mensaje de la operación a registrar.
        
        :type mensaje: str
        """
        with open("root.txt", "a") as log:
            log.write(f"{datetime.datetime.now()}: {mensaje}\n")

class FuncionesBotonera(Exception):
    """- Clase que contiene las funciones para la botonera de la interfaz."""

    def alta(self, nombre, apellido, rubro, cuit, clave_fiscal, tree):
        """- Funcion Alta: Agrega un nuevo cliente a la base de datos y actualiza el Treeview.
        
        :param nombre: Nombre del cliente.

        :param apellido: Apellido del cliente.

        :param rubro: Rubro u oficio del cliente.

        :param cuit: CUIT/CUIL del cliente.

        :param clave_fiscal: Clave fiscal del cliente.

        :param tree: Treeview que se debe actualizar.
        """
        if not self.validar_campos(nombre, apellido, rubro, cuit, clave_fiscal):
            ManejoErrores.registrar_error("Por favor, complete todos los campos.")
            return

        try:
            noticia = Clientes.create(
                nombre=nombre.get(),
                apellido=apellido.get(),
                rubro=rubro.get(),
                cuit=cuit.get(),
                clave_fiscal=clave_fiscal.get()
            )

            ManejoErrores.registrar_movimiento(f"Haz agregado un nuevo cliente llamado/a {noticia.nombre} {noticia.apellido} con CUIT: {noticia.cuit}.")
            self.actualizar_treeview(tree)
        except Exception as e:
            ManejoErrores.registrar_error(str(e))

    def toggle_password(self, show_password_var, entry, show_char):
        """- Funcion ver/o no ver pass: Muestra u oculta la contraseña en el campo de entrada.

        :param show_password_var: Variable de control para mostrar u ocultar la contraseña.

        :param entry: Campo de entrada de la contraseña.

        :param show_char: Carácter a mostrar en lugar de la contraseña.

        """
        if show_password_var.get():
            entry.config(show="")
        else:
            entry.config(show=show_char)

    def abrir_afip(self):
        """- Funcion para direccion a AFIP: Abre la página de AFIP en un navegador web.
        
        Utilizacion de webbrowser, acceso directo hacia la pagina para el registro.
        """
        webbrowser.open("https://www.afip.gob.ar/landing/default.asp")

    def actualizar_treeview(self, mi_tree_view):
        """- Funcion de actulaizar: Actualiza el Treeview con los registros de la base de datos.
        
        :param mi_tree_view: Treeview que se debe actualizar.
        
        """
        records = mi_tree_view.get_children()
        for element in records:
            mi_tree_view.delete(element)

        for fila in Clientes.select():
            mi_tree_view.insert("", 0, text=fila.id, values=(fila.nombre, fila.apellido, fila.rubro, fila.cuit, fila.clave_fiscal))

    def borrar(self, tree):
        """- Funcion borrar cliente: Elimina un cliente seleccionado del Treeview y de la base de datos.
        
        :param tree: Treeview que contiene al cliente a eliminar.
        """
        valor = tree.selection()
        if not valor:
            ManejoErrores.registrar_error("Por favor, seleccione un cliente para eliminar.")
            return

        respuesta = askquestion("Confirmar", "¿Estás seguro que deseas eliminar este cliente?")
        if respuesta == 'yes':
            item = tree.item(valor)
            nombre = item['values'][0]
            apellido = item['values'][1]
            cuit = item['values'][3]
            borrado = Clientes.get(Clientes.nombre == nombre, Clientes.apellido == apellido, Clientes.cuit == cuit)
            borrado.delete_instance()
            tree.delete(valor)
            ManejoErrores.registrar_movimiento(f"Cliente {nombre} {apellido} con CUIT {cuit} eliminado correctamente.")

    def modificar(self, tree, nombre, apellido, rubro, cuit, clave_fiscal):
        """- Funcion Modificar clientes: Modifica los datos de un cliente seleccionado en el Treeview y en la base de datos.

        :param tree: Treeview que contiene al cliente a modificar.

        :param nombre: Nuevo nombre del cliente.

        :param apellido: Nuevo apellido del cliente.

        :param rubro: Nuevo rubro u oficio del cliente.

        :param cuit: Nuevo CUIT/CUIL del cliente.

        :param clave_fiscal: Nueva clave fiscal del cliente.
        
        """
        if not self.validar_campos(nombre, apellido, rubro, cuit, clave_fiscal):
            ManejoErrores.registrar_error("Por favor, complete todos los campos para modificar un cliente.")
            return

        valor = tree.selection()
        if not valor:
            ManejoErrores.registrar_error("Por favor, seleccione un cliente para modificar.")
            return

        item = tree.item(valor)
        nombre_actual = item['values'][0]
        apellido_actual = item['values'][1]
        cuit_actual = item['values'][3]

        respuesta = askquestion("Confirmar", f"¿Estás seguro que deseas modificar al cliente {nombre_actual} {apellido_actual} con CUIT {cuit_actual}.?")
        if respuesta == 'yes':
            nombre_antiguo = nombre_actual
            apellido_antiguo = apellido_actual
            cuit_antiguo = cuit_actual

            actualizar = Clientes.update(
                nombre=nombre.get(),
                apellido=apellido.get(),
                rubro=rubro.get(),
                cuit=cuit.get(),
                clave_fiscal=clave_fiscal.get()
            ).where(Clientes.nombre == nombre_actual, Clientes.apellido == apellido_actual, Clientes.cuit == cuit_actual)
            actualizar.execute()

            nombre_nuevo = nombre.get()
            apellido_nuevo = apellido.get()
            cuit_nuevo = cuit.get()

            ManejoErrores.registrar_movimiento(f"Cliente {nombre_antiguo} {apellido_antiguo} con CUIT {cuit_antiguo} modificado a {nombre_nuevo} {apellido_nuevo} con CUIT {cuit_nuevo}")
            self.actualizar_treeview(tree)

    def consultar(self, tree, nombre, apellido, rubro, cuit, clave_fiscal):
        """- Funcion Consultamos: Consulta los datos de un cliente seleccionado en el Treeview.
        
        :param tree: Treeview que contiene al cliente a consultar.

        :param nombre: Variable para almacenar el nombre del cliente consultado.

        :param apellido: Variable para almacenar el apellido del cliente consultado.

        :param rubro: Variable para almacenar el rubro u oficio del cliente consultado.
        
        :param cuit: Variable para almacenar el CUIT/CUIL del cliente consultado.

        :param clave_fiscal: Variable para almacenar la clave fiscal del cliente consultado.
        
        """
        valor = tree.selection()
        if not valor:
            ManejoErrores.registrar_error("Por favor, seleccione un cliente para consultar.")
            return

        item = tree.item(valor)
        nombre_actual = item['values'][0]
        apellido_actual = item['values'][1]
        cuit_actual = item['values'][3]
        consulta = Clientes.get(Clientes.nombre == nombre_actual, Clientes.apellido == apellido_actual, Clientes.cuit == cuit_actual)

        nombre.set(consulta.nombre)
        apellido.set(consulta.apellido)
        rubro.set(consulta.rubro)
        cuit.set(consulta.cuit)
        clave_fiscal.set(consulta.clave_fiscal)
        ManejoErrores.registrar_movimiento(f"Consulta de cliente {nombre_actual} {apellido_actual} con CUIT {cuit_actual}.")

    def mostrar_mensaje(self, titulo, mensaje):
        """- Funcion para mensajes emergentes: Muestra un mensaje de información.
        
        :param titulo: Título del mensaje.

        :param mensaje: Contenido del mensaje.

        
        """
        showinfo(titulo, mensaje)

    def maximizar_minimizar_ventana(self, tree):
        """- Funcion minimizar y maximizar: Maximiza o minimiza la ventana.
        
        :param tree: Treeview para ocultar o mostrar en la ventana.
        
        """
        if tree.winfo_ismapped():
            tree.grid_remove()
        else:
            tree.grid()

    def validar_campos(self, nombre, apellido, rubro, cuit, clave_fiscal):
        """- Funcion para Validar: Valida que todos los campos estén completos.
        
        :param nombre: Nombre del cliente.

        :param apellido: Apellido del cliente.

        :param rubro: Rubro u oficio del cliente.

        :param cuit: CUIT/CUIL del cliente.

        :param clave_fiscal: Clave fiscal del cliente.

        :returns: True si todos los campos están completos, False en caso contrario.
        """
        if not all([nombre.get(), apellido.get(), rubro.get(), cuit.get(), clave_fiscal.get()]):
            showerror("Error", "Todos los campos son obligatorios")
            return False
        return True
