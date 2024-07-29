import platform
import subprocess
import os
import urllib.request
import sys
import ctypes
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMessageBox

"""
Este módulo proporciona funciones para gestionar la instalación de dependencias necesarias para el proyecto,
así como para verificar y manejar la instalación de software adicional requerido en diferentes sistemas operativos.

Funciones incluidas:

1. **is_admin()**: Verifica si el script se está ejecutando con privilegios de administrador en Windows.

2. **run_as_admin()**: Intenta elevar los privilegios del script a administrador en Windows.

3. **install_python_dependencies()**: Instala las dependencias de Python especificadas en el archivo `requirements.txt`.

4. **ensure_all_dependencies()**: Verifica e instala todas las dependencias necesarias, incluyendo VLC y FFmpeg.

5. **install_vlc_windows()**: Descarga e instala VLC en sistemas Windows si no está presente.

6. **get_vlc_path()**: Obtiene la ruta del ejecutable de VLC en sistemas Windows.

7. **install_vlc_mac()**: Instala VLC en sistemas macOS usando Homebrew.

8. **install_vlc_linux()**: Instala VLC en sistemas Linux (Debian/Ubuntu) usando APT.

9. **ensure_vlc_installed()**: Verifica e instala VLC en el sistema operativo correspondiente.

10. **show_ffmpeg_install_message()**: Muestra un mensaje al usuario de Windows sobre cómo instalar FFmpeg.

11. **install_ffmpeg_windows()**: Muestra un mensaje de instalación de FFmpeg en Windows.

12. **install_ffmpeg_mac()**: Instala FFmpeg en sistemas macOS usando Homebrew.

13. **install_ffmpeg_linux()**: Instala FFmpeg en sistemas Linux (Debian/Ubuntu) usando APT.

14. **ensure_ffmpeg_installed()**: Verifica e instala FFmpeg en el sistema operativo correspondiente.

Al iniciar el script, se verifica si el sistema operativo es Windows y si el script tiene privilegios de administrador. Luego, se asegura que todas las dependencias necesarias estén instaladas.
"""

# Función para verificar y elevar privilegios en Windows
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if is_admin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return False

# Función para instalar dependencias de Python desde un archivo requirements.txt
def install_python_dependencies():
    requirements_path = Path(__file__).parent / 'requirements.txt'
    print(f"Instalando dependencias desde {requirements_path}")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_path)], check=True)
        print("Dependencias instaladas correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar dependencias: {e}")
        sys.exit(1)

# Función para verificar e instalar todas las dependencias necesarias
def ensure_all_dependencies():
    install_python_dependencies()
    ensure_vlc_installed()
    ensure_ffmpeg_installed()

# Función para instalar VLC en Windows
def install_vlc_windows():
    vlc_installer_url = "https://get.videolan.org/vlc/3.0.16/win64/vlc-3.0.16-win64.exe"
    installer_path = Path(__file__).parent / "vlc_installer.exe"
    print(f"Descargando VLC desde {vlc_installer_url} a {installer_path}")
    urllib.request.urlretrieve(vlc_installer_url, installer_path)
    print(f"Ejecutando instalador de VLC desde {installer_path}")
    subprocess.run([str(installer_path), '/S'], check=True)
    os.remove(installer_path)
    print("VLC instalado y archivo instalador eliminado.")

# Función para obtener la ruta del ejecutable VLC en Windows
def get_vlc_path():
    program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
    vlc_path = Path(program_files) / "VideoLAN" / "VLC" / "vlc.exe"
    if not vlc_path.exists():
        program_files_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        vlc_path = Path(program_files_x86) / "VideoLAN" / "VLC" / "vlc.exe"
    return vlc_path

# Función para instalar VLC en macOS
def install_vlc_mac():
    try:
        subprocess.run(['brew', '--version'], check=True)
    except FileNotFoundError:
        subprocess.run(['/bin/bash', '-c', "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"], check=True)
    subprocess.run(['brew', 'install', 'vlc'], check=True)

# Función para instalar VLC en Linux (Debian/Ubuntu)
def install_vlc_linux():
    subprocess.run(['sudo', 'apt', 'update'], check=True)
    subprocess.run(['sudo', 'apt', 'install', '-y', 'vlc'], check=True)

# Función para verificar e instalar VLC en el sistema operativo correspondiente
def ensure_vlc_installed():
    if platform.system() == 'Windows':
        vlc_path = get_vlc_path()
        if not vlc_path.exists():
            install_vlc_windows()
            vlc_path = get_vlc_path()
            if not vlc_path.exists():
                print("Error: VLC no se encontró incluso después de la instalación.")
                sys.exit(1)
        #print(f"VLC encontrado en {vlc_path}")
        # Añadir VLC al PATH temporalmente
        os.environ["PATH"] += os.pathsep + str(vlc_path.parent)
        try:
            subprocess.run([str(vlc_path), '--version'], check=True)
            #print("VLC está instalado y accesible desde la línea de comandos.")
        except subprocess.CalledProcessError:
            print("Error: VLC no se pudo ejecutar correctamente.")
            sys.exit(1)
    elif platform.system() == 'Darwin':
        try:
            subprocess.run(['/Applications/VLC.app/Contents/MacOS/VLC', '--version'], check=True)
        except FileNotFoundError:
            install_vlc_mac()
    elif platform.system() == 'Linux':
        try:
            subprocess.run(['vlc', '--version'], check=True)
        except FileNotFoundError:
            install_vlc_linux()

# Función para mostrar un mensaje al usuario de Windows sobre cómo instalar FFmpeg
def show_ffmpeg_install_message():
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("FFmpeg no encontrado")
    msg.setText("FFmpeg no está instalado en su sistema. Por favor, descárguelo e instálelo desde:\nhttps://ffmpeg.org/download.html")
    msg.setInformativeText("Es importante asegurarse de añadir FFmpeg al PATH del sistema.")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

# Función para instalar FFmpeg en Windows (si se requiere)
def install_ffmpeg_windows():
    show_ffmpeg_install_message()

# Función para instalar FFmpeg en macOS
def install_ffmpeg_mac():
    try:
        subprocess.run(['brew', '--version'], check=True)
    except FileNotFoundError:
        subprocess.run(['/bin/bash', '-c', "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"], check=True)
    subprocess.run(['brew', 'install', 'ffmpeg'], check=True)

# Función para instalar FFmpeg en Linux (Debian/Ubuntu)
def install_ffmpeg_linux():
    subprocess.run(['sudo', 'apt', 'update'], check=True)
    subprocess.run(['sudo', 'apt', 'install', '-y', 'ffmpeg'], check=True)

# Función para verificar e instalar FFmpeg en el sistema operativo correspondiente
def ensure_ffmpeg_installed():
    if platform.system() == 'Windows':
        # No se requiere verificación de FFmpeg en Windows
        pass
    elif platform.system() == 'Darwin':
        try:
            subprocess.run(['ffmpeg', '--version'], check=True)
        except FileNotFoundError:
            install_ffmpeg_mac()
    elif platform.system() == 'Linux':
        try:
            subprocess.run(['ffmpeg', '-version'], check=True)
        except FileNotFoundError:
            install_ffmpeg_linux()

# Llamar a esta función al iniciar el programa para asegurarse de que todas las dependencias estén instaladas
if __name__ == "__main__":
    if platform.system() == 'Windows':
        if not is_admin():
            if not run_as_admin():
                sys.exit(1)
    ensure_all_dependencies()
