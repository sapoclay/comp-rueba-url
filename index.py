# sys se importa para acceder a los argumentos de línea de comandos y para gestionar la terminación del script.
import sys
# QApplication se importa desde PyQt5.QtWidgets para gestionar la aplicación GUI.
from PyQt5.QtWidgets import QApplication
# URLChecker se importa desde url_checker, que se asume es un módulo donde has definido tu clase principal de la interfaz gráfica.
from url_checker import URLChecker

# Este bloque de código se ejecutará solo si el script se ejecuta directamente (no si se importa como módulo).
if __name__ == '__main__':
    # Crea una instancia de QApplication, que es necesaria para cualquier aplicación PyQt5.
    # sys.argv se pasa para permitir que se gestionen los argumentos de línea de comandos.
    app = QApplication(sys.argv)

    # Crea una instancia de la clase URLChecker, que se supone es una ventana o widget principal de la aplicación.
    window = URLChecker()

    # Muestra la ventana o widget en pantalla.
    window.show()

    # Inicia el bucle de eventos de la aplicación, que es necesario para que la aplicación sea interactiva.
    # sys.exit(app.exec_()) asegura que el script termina correctamente al salir del bucle de eventos.
    sys.exit(app.exec_())