import sys
import os
import subprocess
import logging
import platform
import tempfile
import tkinter as tk
from tkinter import simpledialog, messagebox

# Nombre del entorno virtual
VENV_DIR = "venv"

# Creación de archivo .log
def setup_logging():
    try:
        temp_dir = tempfile.gettempdir()
        log_path = os.path.join(temp_dir, 'registro.log')
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path),
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.debug(f"Registro guardado en: {log_path}")
    except Exception as e:
        print(f"Error al configurar el logging: {e}")
        sys.exit(1)

# Función para mostrar mensajes al usuario en una ventana de progreso
def show_progress(message, progress_label, progress_percentage):
    if progress_label:
        progress_label.config(text=f"{progress_percentage}% - {message}")
        progress_label.update_idletasks()

# Función para verificar la instalación de pip y venv, y si es necesario, instalarlos
def check_install_dependencies(password, progress_label):
    try:
        import pip
        logging.debug("pip ya está instalado.")
    except ImportError:
        logging.debug("pip no está instalado.")
        show_progress("Instalando pip...", progress_label, 10)
        install_pip(password)
    
    try:
        import venv
        logging.debug("venv ya está instalado.")
    except ImportError:
        logging.debug("venv no está instalado.")
        show_progress("Instalando venv...", progress_label, 20)
        install_venv(password)

# Instalación de pip
def install_pip(password):
    if platform.system() == 'Windows':
        subprocess.check_call([sys.executable, '-m', 'ensurepip'])
    else:
        install_package(password, 'python3-pip')

# Instalación de venv
def install_venv(password):
    if platform.system() == 'Windows':
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'virtualenv'])
    else:
        install_package(password, 'python3-venv')

# Instalación de paquetes usando apt-get en Ubuntu
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
def find_or_create_venv(progress_label):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    venv_path = os.path.join(script_dir, VENV_DIR)
    
    if not os.path.exists(venv_path):
        create_venv(venv_path, progress_label)
    else:
        logging.debug(f"Entorno virtual encontrado en {venv_path}")
    
    return venv_path

# Creación del entorno virtual
def create_venv(venv_path, progress_label):
    try:
        logging.debug(f"Creando entorno virtual en {venv_path}")
        show_progress("Creando entorno virtual...", progress_label, 30)
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
        logging.debug("Entorno virtual creado correctamente.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al crear el entorno virtual: {e}")
        raise

# Instalación de dependencias del archivo requirements.txt
def install_dependencies(venv_path, progress_label):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        requirements_path = os.path.join(script_dir, 'requirements.txt')
        pip_executable = os.path.join(venv_path, 'bin', 'pip') if os.name == 'posix' else os.path.join(venv_path, 'Scripts', 'pip')
        logging.debug(f"Instalando dependencias desde {requirements_path}")
        show_progress("Instalando dependencias...", progress_label, 50)
        subprocess.check_call([pip_executable, 'install', '-r', requirements_path])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al instalar dependencias: {e}")
        raise

# Instalación de PyQt5 dentro del entorno virtual
def install_pyqt5(venv_path, progress_label):
    try:
        python_executable = os.path.join(venv_path, 'bin', 'python') if os.name == 'posix' else os.path.join(venv_path, 'Scripts', 'python')
        logging.debug("Instalando PyQt5...")
        show_progress("Instalando PyQt5...", progress_label, 70)
        subprocess.check_call([python_executable, '-m', 'pip', 'install', 'pyqt5'])
        logging.debug("PyQt5 instalado correctamente.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al instalar PyQt5: {e}")
        raise

# Verificar la contraseña del usuario actual en Ubuntu
def verify_password(password):
    try:
        # Ejecutar un comando que requiere sudo para verificar la contraseña
        proc = subprocess.run(['sudo', '-S', 'echo', 'Password is correct'],
                              input=password.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            logging.error(f"Contraseña incorrecta: {proc.stderr.decode()}")
            show_error_message("Contraseña incorrecta.")
            return False
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al verificar la contraseña: {e}")
        show_error_message(f"Error al verificar la contraseña: {e}")
        return False

# Pedir la contraseña al usuario mediante tkinter en Windows
def prompt_password():
    if platform.system() == 'Windows':
        return None  # En Windows no se solicita contraseña
    else:
        try:
            result = subprocess.run(['zenity', '--password', '--title=Autenticación requerida'], stdout=subprocess.PIPE)
            password = result.stdout.decode().strip()
            if not password:
                logging.error("No se proporcionó la contraseña.")
                show_error_message("No se proporcionó la contraseña.")
                sys.exit(1)
            if not verify_password(password):
                sys.exit(1)
            return password
        except Exception as e:
            logging.error(f"Error al obtener la contraseña: {e}")
            show_error_message(f"Error al obtener la contraseña: {e}")
            raise

def show_error_message(message):
    if platform.system() == 'Windows':
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", message)
    else:
        subprocess.run(['zenity', '--error', '--title=Error', f'--text={message}'])

def main():
    setup_logging()
    try:
        password = prompt_password()
        
        root = tk.Tk()
        root.title("Instalación en progreso")
        root.geometry("400x200")
        root.resizable(False, False)

        progress_label = tk.Label(root, text="Iniciando instalación...")
        progress_label.pack(pady=20)
        
        root.update_idletasks()

        check_install_dependencies(password, progress_label)
        venv_path = find_or_create_venv(progress_label)
        install_pyqt5(venv_path, progress_label)
        install_dependencies(venv_path, progress_label)
        
        show_progress("Configuración completada. Iniciando la aplicación...", progress_label, 100)

        # Ejecutar el script principal dentro del entorno virtual
        root.quit()  # Añadir esta línea para asegurarse de que el bucle principal termine
        root.update_idletasks()
        root.destroy()  # Añadir esta línea para destruir la ventana antes de continuar
        after_installation(venv_path)
    except Exception as e:
        logging.error(f"Error durante la instalación: {e}")
        print(f"Error durante la instalación: {e}")
        show_error_message(f"Error durante la instalación: {e}")
        sys.exit(1)

# Después de la instalación/comprobación, se lanza el index.py
def after_installation(venv_path):
    try:
        if os.name == 'posix':
            python_executable = os.path.join(venv_path, 'bin', 'python')
        else:
            python_executable = os.path.join(venv_path, 'Scripts', 'pythonw.exe')
            
        index_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'index.py')
        if not os.path.exists(index_path):
            logging.error(f"No se encontró el archivo {index_path}.")
            show_error_message(f"No se encontró el archivo {index_path}.")
            sys.exit(1)

        logging.debug(f"Ejecutando {index_path}...")
        
        if os.name == 'posix':
            process = subprocess.Popen([python_executable, index_path])
        else:
            process = subprocess.Popen([python_executable, index_path], creationflags=subprocess.CREATE_NO_WINDOW)

        # Esperar a que el proceso principal termine
        process.wait()
    except Exception as e:
        logging.error(f"Error al ejecutar index.py: {e}")
        print(f"Error al ejecutar index.py: {e}")
        show_error_message(f"Error al ejecutar index.py: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

