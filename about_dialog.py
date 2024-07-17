from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
import configparser

def obtener_version_actual():
    # Obtener el directorio del archivo que llama a la función
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    # Combinar el directorio con el nombre del archivo config.ini
    ruta_config = os.path.join(directorio_actual, 'config.ini')
    
    config = configparser.ConfigParser()
    config.read(ruta_config)
    return config['Version']['actual']

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('About')
        self.setFixedSize(400, 200)
        layout = QVBoxLayout()

        # Ruta del directorio actual del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, 'logo.png')
        
        # Obtener la versión actual del programa desde el archivo de configuración
        version_actual = obtener_version_actual()

        image_label = QLabel()
        pixmap = QPixmap(logo_path)  # La ruta completa del logo
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        # Formatear la cadena para incluir la versión actual correctamente
        label_text = f"Comp-Rueba-URL.\nVersion: {version_actual}\nDistribuido sin garantías de ningún tipo."
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.setLayout(layout)
