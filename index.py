import sys
import os
import logging
import platform
import tempfile
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from url_checker import URLChecker
from pathlib import Path
from dependencias import ensure_vlc_installed, ensure_ffmpeg_installed, is_admin, run_as_admin

# Directorio del script actual
current_directory = Path(__file__).parent

# Configurar el archivo de registro en un directorio temporal
try:
    temp_dir = tempfile.gettempdir()
    logfile_path = os.path.join(temp_dir, 'registro.log')
    logging.basicConfig(filename=logfile_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Configuración de registro exitosa.")
    #print(f"Archivo de registro configurado en: {logfile_path}")
except Exception as e:
    print(f"Error al configurar el logging: {e}")
    sys.exit(1)

# Función para eliminar listas.txt al salir
def cleanup():
    listas_file = current_directory / 'listas.txt'
    if listas_file.exists():
        listas_file.unlink()
        logging.info("Archivo listas.txt eliminado al salir del programa.")

# Función principal que inicia la aplicación
def main():
    if platform.system() == 'Windows' and not is_admin():
        if not run_as_admin():
            sys.exit(0)

    logging.debug("Inicializando QApplication...")
    app = QApplication(sys.argv)

    # Establecer un icono personalizado
    icon_path = current_directory / 'icono-Comp-Rueba-URL.ico'
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    else:
        logging.warning(f"Icono no encontrado en {icon_path}")
      
    # Verificar e instalar VLC y FFmpeg si no están instalados
    logging.debug("Verificando instalación de VLC...")
    ensure_vlc_installed()
    logging.debug("Verificando instalación de FFmpeg...")
    ensure_ffmpeg_installed()

    logging.debug("Inicializando URLChecker...")
    window = URLChecker()
    window.show()

    # Registrar la función cleanup para que se ejecute al salir
    app.aboutToQuit.connect(cleanup)

    logging.debug("Ejecutando QApplication...")
    sys.exit(app.exec_())

if __name__ == '__main__':
    try:
        logging.debug("Llamada a main()")
        main()
    except Exception as e:
        logging.error(f"Error en la ejecución: {e}", exc_info=True)
        print(f"Error en la ejecución: {e}")
