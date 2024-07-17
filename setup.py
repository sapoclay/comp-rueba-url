import sys
import os
import subprocess
import logging

# Nombre del entorno virtual
VENV_DIR = "venv"

# Creación de archivo .log
def setup_logging():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(script_dir, 'registro.log')
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.debug(f"Registro guardado en: {log_path}")

# Función para mostrar mensajes al usuario en una ventana de progreso
def show_progress(message, progress_proc, progress_percentage):
    progress_proc.stdin.write(f"{progress_percentage}\n# {message}\n")
    progress_proc.stdin.flush()

# Función para verificar la instalación de pip y python3-venv, y si es necesario, instalarlos
def check_install_dependencies(password, progress_proc):
    try:
        import pip
        logging.debug("pip ya está instalado.")
    except ImportError:
        logging.debug("pip no está instalado.")
        show_progress("Instalando pip...", progress_proc, 10)
        install_package(password, 'python3-pip')

    if not os.path.exists('/usr/lib/python3.12/venv'):
        logging.debug("python3-venv no está instalado.")
        show_progress("Instalando python3-venv...", progress_proc, 20)
        install_package(password, 'python3-venv')
    else:
        logging.debug("python3-venv ya está instalado.")

# Instalación de paquetes usando apt-get
def install_package(password, package_name):
    try:
        proc = subprocess.run(['sudo', '-S', 'apt-get', 'install', '-y', package_name],
                              input=password.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            logging.error(f"No se pudo instalar {package_name}: {proc.stderr.decode()}")
            raise subprocess.CalledProcessError(proc.returncode, proc.args)
        logging.debug(f"{package_name} instalado correctamente.")
    except subprocess.CalledProcessError as e:
        logging.error(f"No se pudo instalar {package_name}: {e}")
        raise

# Buscar o crear el entorno virtual en el que ejecutar el programa
def find_or_create_venv(progress_proc):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    venv_path = os.path.join(script_dir, VENV_DIR)
    
    if not os.path.exists(venv_path):
        create_venv(venv_path, progress_proc)
    else:
        logging.debug(f"Entorno virtual encontrado en {venv_path}")
    
    return venv_path

# Creación del entorno virtual
def create_venv(venv_path, progress_proc):
    try:
        logging.debug(f"Creando entorno virtual en {venv_path}")
        show_progress("Creando entorno virtual...", progress_proc, 30)
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
        logging.debug("Entorno virtual creado correctamente.")
        # Instalamos pip dentro del entorno virtual para asegurarnos de que esté disponible
        subprocess.check_call([os.path.join(venv_path, 'bin', 'python'), '-m', 'ensurepip', '--default-pip'])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al crear el entorno virtual: {e}")
        raise

# Instalación de dependencias del archivo requirements.txt
def install_dependencies(venv_path, progress_proc):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        requirements_path = os.path.join(script_dir, 'requirements.txt')
        pip_executable = os.path.join(venv_path, 'bin', 'pip') if os.name == 'posix' else os.path.join(venv_path, 'Scripts', 'pip')
        logging.debug(f"Instalando dependencias desde {requirements_path}")
        show_progress("Instalando dependencias...", progress_proc, 50)
        subprocess.check_call([pip_executable, 'install', '-r', requirements_path])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al instalar dependencias: {e}")
        raise

# Instalación de PyQt5 dentro del entorno virtual
def install_pyqt5(venv_path, progress_proc):
    try:
        python_executable = os.path.join(venv_path, 'bin', 'python') if os.name == 'posix' else os.path.join(venv_path, 'Scripts', 'python')
        logging.debug("Instalando PyQt5...")
        show_progress("Instalando PyQt5...", progress_proc, 70)
        subprocess.check_call([python_executable, '-m', 'pip', 'install', 'pyqt5'])
        logging.debug("PyQt5 instalado correctamente.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al instalar PyQt5: {e}")
        raise

# Pedir la contraseña al usuario mediante zenity
def prompt_password():
    try:
        result = subprocess.run(['zenity', '--password', '--title=Autenticación requerida'], stdout=subprocess.PIPE)
        password = result.stdout.decode().strip()
        if not password:
            logging.error("No se proporcionó la contraseña.")
            show_error_message("No se proporcionó la contraseña.")
            sys.exit(1)
        return password
    except Exception as e:
        logging.error(f"Error al obtener la contraseña: {e}")
        show_error_message(f"Error al obtener la contraseña: {e}")
        raise

def show_error_message(message):
    subprocess.run(['zenity', '--error', '--title=Error', f'--text={message}'])

def main():
    setup_logging()
    try:
        password = prompt_password()
        progress_proc = subprocess.Popen(['zenity', '--progress', '--title=Comprobación ...', '--no-cancel', '--auto-close'],
                                         stdin=subprocess.PIPE, text=True)
        
        check_install_dependencies(password, progress_proc)
        venv_path = find_or_create_venv(progress_proc)
        install_pyqt5(venv_path, progress_proc)
        install_dependencies(venv_path, progress_proc)
        
        show_progress("Configuración completada. Iniciando la aplicación...", progress_proc, 100)
        progress_proc.stdin.close()
        progress_proc.wait()

        # Ejecutar el script principal dentro del entorno virtual
        after_installation(venv_path, progress_proc)

    except Exception as e:
        logging.error(f"Error durante la instalación: {e}")
        print(f"Error durante la instalación: {e}")
        show_progress(f"Error durante la instalación: {e}", progress_proc, 100)
        progress_proc.stdin.close()
        progress_proc.wait()
        show_error_message(f"Error durante la instalación: {e}")
        sys.exit(1)

# Después de la instalación/comprobación, se lanza el index.py
def after_installation(venv_path, progress_proc):
    try:
        python_executable = os.path.join(venv_path, 'bin', 'python') if os.name == 'posix' else os.path.join(venv_path, 'Scripts', 'python')
        index_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'index.py')
        if not os.path.exists(index_path):
            logging.error(f"No se encontró el archivo {index_path}.")
            show_progress(f"No se encontró el archivo {index_path}.", progress_proc, 100)
            show_error_message(f"No se encontró el archivo {index_path}.")
            sys.exit(1)
        logging.debug(f"Ejecutando {index_path}...")
        subprocess.call([python_executable, index_path])
    except Exception as e:
        logging.error(f"Error al ejecutar index.py: {e}")
        print(f"Error al ejecutar index.py: {e}")
        show_progress(f"Error al ejecutar index.py: {e}", progress_proc, 100)
        show_error_message(f"Error al ejecutar index.py: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
