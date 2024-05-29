from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        super().__init__()
        self.setWindowTitle('About')
        self.setFixedSize(400, 200)
        layout = QVBoxLayout()

        # Ruta del directorio actual del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, 'logo.png')

        image_label = QLabel()
        pixmap = QPixmap(logo_path)  # La ruta completa del logo
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        label = QLabel("Comp-Rueba-URL.\nVersion 0.5\nDistribuido sin garantías de ningún tipo.")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.setLayout(layout)