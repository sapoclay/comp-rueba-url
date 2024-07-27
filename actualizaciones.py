import os
import configparser
import requests
import wget
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDialog, QInputDialog, QLineEdit
import sys

def obtener_version_actual():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_config = os.path.join(directorio_actual, 'config.ini')

    config = configparser.ConfigParser()
    config.read(ruta_config)
    return config['Version']['actual']

def instalar_paquete_deb(archivo_deb):
    try:
        contrasena_usuario, ok = QInputDialog.getText(None, "Contraseña de usuario",
                                                      "Por favor, ingrese su contraseña de usuario:",
                                                      QLineEdit.Password)
        if not ok or not contrasena_usuario:
            return

        ruta_absoluta = os.path.abspath(archivo_deb)

        comando_instalacion = ['sudo', '-S', 'apt', 'install', ruta_absoluta]

        proceso_instalacion = subprocess.Popen(comando_instalacion, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                               universal_newlines=True)
        _, error = proceso_instalacion.communicate(input=contrasena_usuario + "\n")

        if proceso_instalacion.returncode == 0:
            QMessageBox.information(None, "Instalación exitosa",
                                    "Se ha instalado correctamente la última versión del programa.")
            os.remove(archivo_deb)
            if QMessageBox.question(None, "Reiniciar programa",
                                    "Se requiere reiniciar el programa para aplicar los cambios. ¿Deseas reiniciar ahora?",
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                python = sys.executable
                os.execl(python, python, *sys.argv)
        else:
            QMessageBox.critical(None, "Error de instalación",
                                 f"Error durante la actualización del programa:\n{error}")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error inesperado: {e}")
 
class VentanaActualizaciones(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Buscar Actualizaciones")
        self.setGeometry(100, 100, 500, 200)
        self.setFixedSize(500, 200)

        version_actual = obtener_version_actual()

        self.version_instalada_label = QLabel(f"Versión instalada: {version_actual}", self)

        self.boton_comprobar = QPushButton("Buscar e Instalar Actualizaciones", self)
        self.boton_comprobar.clicked.connect(self.comprobar_actualizaciones)

        self.etiqueta_estado = QLabel("", self)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.version_instalada_label)
        layout_principal.addWidget(self.boton_comprobar)
        layout_principal.addWidget(self.etiqueta_estado)

        self.setLayout(layout_principal)

    def comprobar_actualizaciones(self):
        try:
            usuario = 'sapoclay'
            repositorio = 'comp-rueba-url'
            url_repositorio = f'https://api.github.com/repos/{usuario}/{repositorio}/releases/latest'

            respuesta = requests.get(url_repositorio)
            respuesta_json = respuesta.json()

            version_mas_reciente = respuesta_json['tag_name']
            version_actual = obtener_version_actual()

            if version_mas_reciente <= version_actual:
                QMessageBox.information(None, "Sin actualizaciones",
                                        "No hay actualizaciones disponibles en este momento.")
                return  # Abortar la función si no hay actualizaciones

            mensaje_resultado = f"Versión actual instalada: {version_actual}\nLa versión más reciente disponible es: {version_mas_reciente}"
            self.etiqueta_estado.setText(mensaje_resultado)
            url_descarga = respuesta_json['assets'][0]['browser_download_url']
            ruta_home = os.path.expanduser("~")
            archivo_descargado = os.path.join(ruta_home, "Comp-Rueba-URL.deb")

            wget.download(url_descarga, archivo_descargado)
            instalar_paquete_deb(archivo_descargado)

            self.etiqueta_estado.setText("Actualización exitosa.")

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_actualizaciones = VentanaActualizaciones()
    ventana_actualizaciones.exec_()
