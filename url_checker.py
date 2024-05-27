from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QMenuBar, QAction, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSlot
import subprocess
import platform
from url_check_worker import URLCheckWorker
from about_dialog import AboutDialog
from url_utilities import getStreamURL

class URLChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.url_check_thread = QThread()
        self.url_check_worker = URLCheckWorker()
        self.url_check_worker.moveToThread(self.url_check_thread)
        self.url_check_worker.url_checked.connect(self.handleURLChecked)
        self.url_check_thread.start()

    @pyqtSlot(bool)
    def handleURLChecked(self, is_available):
        if is_available:
            self.result_label.setText('URL activa')
            self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: green;")
            self.open_vlc_button.setVisible(True)
            self.url_to_open = self.url_input.text().strip()
        else:
            self.result_label.setText('URL no disponible')
            self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: red;")
            self.open_vlc_button.setVisible(False)

    def initUI(self):
        self.setWindowTitle('Comp-Rueba-URL')
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()
        menubar = QMenuBar(self)
        file_menu = menubar.addMenu('Archivo')
        exit_action = QAction('Salir', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        options_menu = menubar.addMenu('Opciones')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.showAboutDialog)
        options_menu.addAction(about_action)
        layout.setMenuBar(menubar)
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)
        button_layout = QHBoxLayout()
        self.check_button = QPushButton('Comprobar URL')
        self.check_button.setToolTip('Comprueba si la URL proporcionada está activa y es un archivo m3u8, m3u, .ts o un flujo de transmisión multimedia')
        self.check_button.clicked.connect(self.checkURL)
        button_layout.addWidget(self.check_button)
        self.clear_button = QPushButton('Borrar URL')
        self.clear_button.setToolTip('Borra el contenido del campo de entrada de URL')
        self.clear_button.clicked.connect(self.clearURL)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: blue;")
        layout.addWidget(self.result_label)
        self.open_vlc_button = QPushButton('Abrir en VLC')
        self.open_vlc_button.setToolTip('Abre la URL en VLC Media Player')
        self.open_vlc_button.clicked.connect(self.openInVLC)
        self.open_vlc_button.setVisible(False)
        layout.addWidget(self.open_vlc_button)
        self.setLayout(layout)

    def checkURL(self):
        url = self.url_input.text().strip()
        self.url_input.setText(url)
        self.result_label.setText('Verificando URL...')
        self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: blue;")

        # Emite la señal para verificar la URL en el hilo del trabajador
        self.url_check_worker.check_url_signal.emit(url)

    def clearURL(self):
        self.url_input.clear()
        self.result_label.clear()
        self.open_vlc_button.setVisible(False)

    def isVLCInstalled(self):
        try:
            if platform.system() == 'Windows':
                subprocess.run(['vlc', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            elif platform.system() == 'Darwin':
                subprocess.run(['/Applications/VLC.app/Contents/MacOS/VLC', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            elif platform.system() == 'Linux':
                subprocess.run(['vlc', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            return False
    @classmethod
    def isVLCInstalled(cls):
        try:
            if platform.system() == 'Windows':
                subprocess.run(['vlc', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            elif platform.system() == 'Darwin':
                subprocess.run(['/Applications/VLC.app/Contents/MacOS/VLC', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            elif platform.system() == 'Linux':
                subprocess.run(['vlc', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            return False

    def openInVLC(self):
        url = self.url_to_open
        stream_url = getStreamURL(url)
        if stream_url is None:
            QMessageBox.critical(self, "Error", "No se pudo obtener la URL de streaming.")
            return
        if not self.isVLCInstalled():
            if not self.installVLC():
                return
        try:
            if platform.system() == 'Windows':
                subprocess.Popen(['vlc', stream_url])
            elif platform.system() == 'Darwin':
                subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC', stream_url])
            elif platform.system() == 'Linux':
                subprocess.Popen(['vlc', stream_url])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fallo al abrir VLC: {str(e)}")

    def showAboutDialog(self):
        about_dialog = AboutDialog()
        about_dialog.exec_()