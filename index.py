import sys
import os
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from url_checker import URLChecker
from pathlib import Path
from dependencias import ensure_vlc_installed, ensure_ffmpeg_installed

# Directorio del script actual
current_directory = Path(__file__).parent

# Configurar el archivo de registro en el directorio del script
logfile_path = current_directory / 'registro.log'
logging.basicConfig(filename=logfile_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Configuración de registro exitosa.")

# Función para eliminar listas.txt al salir
def cleanup():
    listas_file = current_directory / 'listas.txt'
    if listas_file.exists():
        listas_file.unlink()
        logging.info("Archivo listas.txt eliminado al salir del programa.")

# Función principal que inicia la aplicación
def main():
    app = QApplication(sys.argv)
    
    # Establecer un icono personalizado
    icon_path = current_directory / 'icono-Comp-Rueba-URL.png'
    app.setWindowIcon(QIcon(str(icon_path)))
      
    # Verificar e instalar VLC y FFmpeg si no están instalados
    ensure_vlc_installed()
    ensure_ffmpeg_installed()

    window = URLChecker()
    window.show()

    # Registrar la función cleanup para que se ejecute al salir
    app.aboutToQuit.connect(cleanup)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()