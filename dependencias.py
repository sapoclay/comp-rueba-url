import platform
import subprocess
import os
import urllib.request

# Función para instalar VLC en Windows
def install_vlc_windows():
    vlc_installer_url = "https://get.videolan.org/vlc/3.0.16/win64/vlc-3.0.16-win64.exe"
    installer_path = "vlc_installer.exe"
    urllib.request.urlretrieve(vlc_installer_url, installer_path)
    subprocess.run([installer_path, '/S'], check=True)
    os.remove(installer_path)

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
        try:
            subprocess.run(['vlc', '--version'], check=True)
        except FileNotFoundError:
            install_vlc_windows()
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

# Función para instalar dependencias de Python desde un archivo requirements.txt
def install_python_dependencies():
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)

# Función para verificar e instalar todas las dependencias necesarias
def ensure_all_dependencies():
    install_python_dependencies()
    ensure_vlc_installed()

# Llamar a esta función al iniciar el programa para asegurarse de que todas las dependencias estén instaladas
if __name__ == "__main__":
    ensure_all_dependencies()