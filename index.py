# Importar la función de verificación de dependencias
from dependencias import ensure_all_dependencies
import logging


# Configurar logging para registrar errores
logfile_path = '/usr/share/Comp-Rueba-URL/logfile.log'
logging.basicConfig(filename=logfile_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

import atexit
import os
import sys
from PyQt5.QtWidgets import QApplication
from url_checker import URLChecker

# Verificar e instalar todas las dependencias necesarias
ensure_all_dependencies()

# Función para eliminar listas.txt al salir
def cleanup():
    listas_file = 'listas.txt'
    if os.path.exists(listas_file):
        os.remove(listas_file)
        logging.info("Archivo listas.txt eliminado al salir del programa.")

# Registrar la función cleanup para que se ejecute al salir
atexit.register(cleanup)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        url_checker = URLChecker()
        url_checker.show()
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Error al ejecutar la aplicación: {str(e)}")
        sys.exit(1)