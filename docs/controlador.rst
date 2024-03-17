Controlador
==================

.. note::
   
   Permite el lanzamiento de la aplicacion contable interaccion con la vista y modelo.

Modulos Importados
--------------------

.. code-block:: python
 
   import tkinter as tk
   """- Importamos el módulo tkinter y lo renombramos como tk."""

   import vista
   """- Se importa el modulo vista, que contiene la clase VistaPrincipal y Clock."""


Clases
--------------------
.. note::
   
   La clase `Controller` actúa como el controlador principal de la aplicación, gestionando la lógica de negocio y la interacción entre la vista y el modelo. Se encarga de manejar los eventos generados por la interfaz gráfica y de actualizar la base de datos según las acciones del usuario.
   Esta clase se comunica con la clase `FuncionesBotonera` del modelo para realizar operaciones como agregar, eliminar y modificar clientes, y también se encarga de actualizar la vista en consecuencia. Su objetivo es mantener la coherencia entre los datos almacenados y la interfaz gráfica, asegurando una experiencia de usuario fluida y consistente.


.. automodule:: controlador


.. rubric:: :: Controller
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Este código define la clase Controller, que actúa como el controlador principal de la aplicación. Al inicializarse, crea una instancia de la clase Tk de Tkinter para representar la ventana principal de la aplicación. Luego, crea una instancia de la clase VistaPrincipal del módulo vista (que representa la interfaz gráfica principal) y otra instancia de la clase Clock del mismo módulo (que representa un reloj en la parte inferior de la aplicación). Finalmente, inicia el bucle principal de eventos de la interfaz gráfica con el método mainloop() de la instancia Tk, lo que permite que la aplicación responda a las interacciones del usuario.

.. autoclass:: Controller
   :members:
   :undoc-members:

.. image:: ./i1.png

.. code-block:: python

   class Controller():
      """- Clase Controller: Controlador principal de la aplicación. """
      def __init__(self, root_w):
         """
         Inicializa el controlador.
         """
         self.root = root_w
         self.objeto_vista = vista.VistaPrincipal(self.root)
         self.clock = vista.Clock(self.root)

         #root_w (Tk): Instancia de la clase Tk de Tkinter, representa la ventana principal de la aplicación.
         #root (Tk): Ventana principal de la aplicación.
         #objeto_vista (vista.VistaPrincipal): Objeto de la clase VistaPrincipal que representa la vista principal de la aplicación
         #clock (vista.Clock): Objeto de la clase Clock que representa el reloj en la parte inferior de la aplicación.

   if __name__ == "__main__":
      root = Tk()  # Se crea una instancia de la clase Tk para representar la ventana principal
      aplicacion = Controller(root)  # Se crea una instancia de la clase Controller
      root.mainloop()  # Se inicia el bucle principal de eventos de la interfaz gráfica
