# Modulos importados
from tkinter import Tk  # Se importa la clase Tk de Tkinter
import vista  # Se importa el modulo vista, que contiene la clase VistaPrincipal y Clock

class Controller():
    """
    - Clase Controller: Controlador principal de la aplicación.

    Args:
        root_w (Tk): Instancia de la clase Tk de Tkinter, representa la ventana principal de la aplicación.

    Attributes:
        root (Tk): Ventana principal de la aplicación.
        
        objeto_vista (vista.VistaPrincipal): Objeto de la clase VistaPrincipal que representa la vista principal de la aplicación.

        clock (vista.Clock): Objeto de la clase Clock que representa el reloj en la parte inferior de la aplicación.
    """

    def __init__(self, root_w):
        """
        Inicializa el controlador.

        Args:
            root_w (Tk): Instancia de la clase Tk de Tkinter, representa la ventana principal de la aplicación.
        """
        self.root = root_w
        self.objeto_vista = vista.VistaPrincipal(self.root)
        self.clock = vista.Clock(self.root)

if __name__ == "__main__":
    root = Tk()  # Se crea una instancia de la clase Tk para representar la ventana principal
    aplicacion = Controller(root)  # Se crea una instancia de la clase Controller
    root.mainloop()  # Se inicia el bucle principal de eventos de la interfaz gráfica
