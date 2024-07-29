from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
import configparser

def obtener_version_actual():
    """
    Obtiene la versión actual del programa desde un archivo de configuración.

    Esta función lee el archivo `config.ini` ubicado en el mismo directorio que el script actual
    y devuelve la versión actual especificada en la sección 'Version'.

    Devuelve:
        str: La versión actual del programa.
    """
    # Obtener el directorio del archivo que llama a la función
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    # Combinar el directorio con el nombre del archivo config.ini
    ruta_config = os.path.join(directorio_actual, 'config.ini')
    
    config = configparser.ConfigParser()
    config.read(ruta_config)
    return config['Version']['actual']

class AboutDialog(QDialog):
    """
    Diálogo que muestra información sobre el programa, incluyendo el logo y la versión actual.

    Hereda de QDialog y proporciona una interfaz de usuario con un logo y un mensaje que muestra
    la versión actual del programa. También incluye un botón de "Aceptar" para cerrar el diálogo.

    Métodos:
        __init__(parent=None): Inicializa el diálogo y configura la interfaz de usuario.
        initUI(): Configura los elementos de la interfaz de usuario, incluyendo el logo y la información del programa.
    """
    def __init__(self, parent=None):
        """
        Inicializa el diálogo y configura la interfaz de usuario.

        Argumentos:
            parent (QWidget, optional): El widget padre de este diálogo. Por defecto es None.
        """
        super().__init__(parent)
        self.initUI()

    def initUI(self): 
        """
        Configura los elementos de la interfaz de usuario para el diálogo.
        
        Configura el título del diálogo, el tamaño fijo, y añade un logo y un texto informativo
        que incluye la versión actual del programa. También añade un botón de "Aceptar" para
        cerrar el diálogo.
        """
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
