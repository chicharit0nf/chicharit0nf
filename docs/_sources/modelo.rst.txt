Modelo
==========

.. note::
   
   El archivo de modelo define la estructura de la base de datos utilizada en la aplicación. Contiene la definición de la tabla 'Clientes', que incluye campos como nombre, apellido, rubro, CUIT y clave fiscal. Utiliza la librería Peewee para interactuar con la base de datos SQLite.

Modulos Importados
--------------------

.. code-block:: python

   from tkinter import *
   """- Interfaz estándar de Python para el kit de herramientas Tk GUI. Proporciona clases y funciones para crear interfaces gráficas de usuario."""

   from tkinter.messagebox import *
   """- Proporciona una clase para crear cuadros de diálogo y mostrar mensajes de forma modal. Es útil para mostrar mensajes de error, advertencia o información."""

   from peewee import *
   """- Peewee es un ORM (Mapeo Objeto-Relacional) simple y pequeño para Python. Facilita la interacción con bases de datos relacionales a través de objetos Python."""

   import webbrowser
   """- Proporciona una interfaz para abrir y controlar navegadores web. Útil para abrir URLs en el navegador predeterminado del sistema."""

   import datetime
   """- Proporciona clases para manipular fechas y horas en Python. Permite crear objetos de fecha y hora, y realizar operaciones como comparaciones y cálculos de diferencia."""



Clases
--------------------
.. note::
   
   Estas clases están diseñadas para facilitar el manejo de una base de datos de clientes, asegurando un registro correcto de la información y la interacción con el usuario.

.. automodule:: modelo
   
.. rubric:: :: BaseModel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Clase base para el modelo de la base de datos. Define la configura de la base de datos que será utilizada por el modelo de datos de la aplicación.

.. autoclass:: BaseModel
   :undoc-members:

.. image:: ./i1.png
.. code-block:: python

   class BaseModel(Model):
      """- Clase base para el modelo de la base de datos.
      """
      class Meta():
         """
         :param database: creamos con nombre nuestra base de datos. """
         database = midb




.. rubric:: :: Clientes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Clase que representa la tabla 'Clientes' en la base de datos. Define los campos necesarios para almacenar la información de los clientes, como nombre, apellido, rubro, CUIT y clave fiscal.

.. autoclass:: Clientes
   :members:
   :undoc-members:

.. image:: ./i1.png
.. code-block:: python

   class Clientes(BaseModel):
      """- Clase que representa la tabla 'Clientes' en la base de datos.

      defininimos entonces...
      """
      nombre = CharField()
      apellido = CharField()
      rubro = CharField()
      cuit = IntegerField()
      clave_fiscal = CharField()

      """- Luego se establece la conexion. """

   midb.connect()
   midb.create_tables([Clientes])


.. rubric:: :: ManejoErrores
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Clase que gestiona los registros de errores y operaciones del usuario. Contiene métodos estáticos para registrar errores en archivos de registro y mostrar mensajes de error al usuario.

.. autoclass:: ManejoErrores
   :members:
   :undoc-members:
.. image:: ./i1.png
.. code-block:: python

   class ManejoErrores():
      """- Clase que gestiona los registros de errores y operaciones del usuario."""

      @staticmethod
      def registrar_error(mensaje):
         """- Funcion registro de error: Registra un error en el archivo 'errores.txt' y muestra un mensaje de error.
         """
         error = f"Se ha dado un error, {mensaje}"
         with open("errores.txt", "a") as log:
               log.write(f"{datetime.datetime.now()}: {error}\n")
         showerror("Error", error)

      @staticmethod
      def registrar_movimiento(mensaje):
         """- Funcion registro de accion: Registra una operación del usuario en el archivo 'root.txt'.
         """
         with open("root.txt", "a") as log:
               log.write(f"{datetime.datetime.now()}: {mensaje}\n")



.. rubric:: :: FuncionesBotonera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Proporciona métodos para gestionar la interacción de botones en la interfaz gráfica, como agregar clientes, eliminar clientes y modificar datos de clientes en una base de datos. Estos métodos facilitan el manejo de eventos de usuario y la actualización de la interfaz en una aplicación de gestión de clientes.

.. autoclass:: FuncionesBotonera
   :members:
   :undoc-members:

   :show-inheritance:

.. image:: ./i1.png
.. code-block:: python

   class FuncionesBotonera(Exception):
      """- Clase que contiene las funciones para la botonera de la interfaz."""

      def alta(self, nombre, apellido, rubro, cuit, clave_fiscal, tree):
         """- Funcion Alta: Agrega un nuevo cliente a la base de datos y actualiza el Treeview.
         
         Este if verifica si la función validar_campos devuelve False, lo que significa que uno o más campos no están completos. 
         En ese caso, se muestra un mensaje de error y la función alta retorna, evitando que se ejecute el código restante.
         """
         if not self.validar_campos(nombre, apellido, rubro, cuit, clave_fiscal):
               ManejoErrores.registrar_error("Por favor, complete todos los campos.")
               return

         try:                                                #lanza la excepcion
               noticia = Clientes.create(
                  nombre=nombre.get(),
                  apellido=apellido.get(),                  #Con el .get() llamamos cuando ahce el alta.
                  rubro=rubro.get(),
                  cuit=cuit.get(),
                  clave_fiscal=clave_fiscal.get()
               )

               ManejoErrores.registrar_movimiento(f"Haz agregado un nuevo cliente llamado/a {noticia.nombre} {noticia.apellido} con CUIT: {noticia.cuit}.")
               self.actualizar_treeview(tree)             #(Notificacion en el .txt)
         except Exception as e:
               ManejoErrores.registrar_error(str(e))      #Caso contrario Notifica el error.

   def toggle_password(self, show_password_var, entry, show_char):
      """- Funcion ver/o no ver pass: Muestra u oculta la contraseña en el campo de entrada.
      """
      if show_password_var.get():  # Si la variable show_password_var es True
         entry.config(show="")  # Configura el campo de entrada para mostrar la contraseña
      else:
         entry.config(show=show_char)  # Configura el campo de entrada para ocultar la contraseña

   def abrir_afip(self):
      """- Funcion para direccion a AFIP: Abre la página de AFIP en un navegador web.
      
      Utilización de webbrowser, acceso directo hacia la página para el registro.
      """
      webbrowser.open("https://www.afip.gob.ar/landing/default.asp")  # Abre la página de AFIP en un navegador web

   def actualizar_treeview(self, mi_tree_view):
      """- Funcion de actulaizar: Actualiza el Treeview con los registros de la base de datos.
      """
      records = mi_tree_view.get_children()  # Obtiene los registros actuales del Treeview
      for element in records:
         mi_tree_view.delete(element)  # Borra todos los registros actuales del Treeview

      for fila in Clientes.select():  # Itera sobre todos los registros de la tabla Clientes
         mi_tree_view.insert("", 0, text=fila.id, values=(fila.nombre, fila.apellido, fila.rubro, fila.cuit, fila.clave_fiscal))  # Inserta cada registro en el Treeview

   def borrar(self, tree):
      """- Funcion borrar cliente: Elimina un cliente seleccionado del Treeview y de la base de datos.
      """
      valor = tree.selection()  # Obtiene el valor seleccionado en el Treeview
      if not valor:  # Si no hay ningún valor seleccionado
         ManejoErrores.registrar_error("Por favor, seleccione un cliente para eliminar.")  # Muestra un mensaje de error
         return

      respuesta = askquestion("Confirmar", "¿Estás seguro que deseas eliminar este cliente?")  # Muestra un cuadro de diálogo de confirmación
      if respuesta == 'yes':  # Si el usuario confirma la eliminación
         item = tree.item(valor)  # Obtiene el ítem seleccionado en el Treeview
         nombre = item['values'][0]  # Obtiene el nombre del cliente a eliminar
         apellido = item['values'][1]  # Obtiene el apellido del cliente a eliminar
         cuit = item['values'][3]  # Obtiene el CUIT del cliente a eliminar
         borrado = Clientes.get(Clientes.nombre == nombre, Clientes.apellido == apellido, Clientes.cuit == cuit)  # Obtiene el registro de la base de datos correspondiente al cliente a eliminar
         borrado.delete_instance()  # Elimina el registro de la base de datos
         tree.delete(valor)  # Elimina el cliente seleccionado del Treeview
         ManejoErrores.registrar_movimiento(f"Cliente {nombre} {apellido} con CUIT {cuit} eliminado correctamente.")  # Registra la eliminación en el registro de movimientos

   def modificar(self, tree, nombre, apellido, rubro, cuit, clave_fiscal):
      """- Funcion Modificar clientes: Modifica los datos de un cliente seleccionado en el Treeview y en la base de datos.
      """
      if not self.validar_campos(nombre, apellido, rubro, cuit, clave_fiscal):  # Si los campos no están completos
         ManejoErrores.registrar_error("Por favor, complete todos los campos para modificar un cliente.")  # Muestra un mensaje de error
         return

      valor = tree.selection()  # Obtiene el valor seleccionado en el Treeview
      if not valor:  # Si no hay ningún valor seleccionado
         ManejoErrores.registrar_error("Por favor, seleccione un cliente para modificar.")  # Muestra un mensaje de error
         return

      item = tree.item(valor)  # Obtiene el ítem seleccionado en el Treeview
      nombre_actual = item['values'][0]  # Obtiene el nombre actual del cliente
      apellido_actual = item['values'][1]  # Obtiene el apellido actual del cliente
      cuit_actual = item['values'][3]  # Obtiene el CUIT actual del cliente

      respuesta = askquestion("Confirmar", f"¿Estás seguro que deseas modificar al cliente {nombre_actual} {apellido_actual} con CUIT {cuit_actual}.?")  # Muestra un cuadro de diálogo de confirmación
      if respuesta == 'yes':  # Si el usuario confirma la modificación
         nombre_antiguo = nombre_actual  # Guarda el nombre antiguo del cliente
         apellido_antiguo = apellido_actual  # Guarda el apellido antiguo del cliente
         cuit_antiguo = cuit_actual  # Guarda el CUIT antiguo del cliente

         # Actualiza los datos del cliente en la base de datos
         actualizar = Clientes.update(
               nombre=nombre.get(),
               apellido=apellido.get(),
               rubro=rubro.get(),
               cuit=cuit.get(),
               clave_fiscal=clave_fiscal.get()
         ).where(Clientes.nombre == nombre_actual, Clientes.apellido == apellido_actual, Clientes.cuit == cuit_actual)
         actualizar.execute()

         nombre_nuevo = nombre.get()  # Obtiene el nuevo nombre del cliente
         apellido_nuevo = apellido.get()  # Obtiene el nuevo apellido del cliente
         cuit_nuevo = cuit.get()  # Obtiene el nuevo CUIT del cliente

         ManejoErrores.registrar_movimiento(f"Cliente {nombre_antiguo} {apellido_antiguo} con CUIT {cuit_antiguo} modificado a {nombre_nuevo} {apellido_nuevo} con CUIT {cuit_nuevo}")  # Registra la modificación en el registro de movimientos
         self.actualizar_treeview(tree)  # Actualiza el Treeview

   def consultar(self, tree, nombre, apellido, rubro, cuit, clave_fiscal):
      """- Funcion Consultamos: Consulta los datos de un cliente seleccionado en el Treeview.
      """
      valor = tree.selection()  # Obtiene el valor seleccionado en el Treeview
      if not valor:  # Si no hay ningún valor seleccionado
         ManejoErrores.registrar_error("Por favor, seleccione un cliente para consultar.")  # Muestra un mensaje de error
         return

      item = tree.item(valor)  # Obtiene el ítem seleccionado en el Treeview
      nombre_actual = item['values'][0]  # Obtiene el nombre actual del cliente
      apellido_actual = item['values'][1]  # Obtiene el apellido actual del cliente
      cuit_actual = item['values'][3]  # Obtiene el CUIT actual del cliente
      consulta = Clientes.get(Clientes.nombre == nombre_actual, Clientes.apellido == apellido_actual, Clientes.cuit == cuit_actual)  # Realiza la consulta en la base de datos

      # Establece los valores de los campos en la interfaz con los datos consultados
      nombre.set(consulta.nombre)
      apellido.set(consulta.apellido)
      rubro.set(consulta.rubro)
      cuit.set(consulta.cuit)
      clave_fiscal.set(consulta.clave_fiscal)
      ManejoErrores.registrar_movimiento(f"Consulta de cliente {nombre_actual} {apellido_actual} con CUIT {cuit_actual}.")  # Registra la consulta en el registro de movimientos

   def mostrar_mensaje(self, titulo, mensaje):
      """- Funcion para mensajes emergentes: Muestra un mensaje de información.
      """
      showinfo(titulo, mensaje)  # Muestra un cuadro de diálogo con un mensaje de información

   def maximizar_minimizar_ventana(self, tree):
      """- Funcion minimizar y maximizar: Maximiza o minimiza la ventana.
      """
      if tree.winfo_ismapped():  # Si la ventana está visible
         tree.grid_remove()  # Remueve la ventana
      else:
         tree.grid()  # Muestra la ventana

   def validar_campos(self, nombre, apellido, rubro, cuit, clave_fiscal):
      """- Funcion para Validar: Valida que todos los campos estén completos.
      """
      if not all([nombre.get(), apellido.get(), rubro.get(), cuit.get(), clave_fiscal.get()]):  # Si alguno de los campos está vacío
         showerror("Error", "Todos los campos son obligatorios")  # Muestra un mensaje de error
         return False  # Retorna False indicando que la validación falló
      return True  # Retorna True indicando que la validación fue exitosa

