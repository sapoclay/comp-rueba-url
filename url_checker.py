from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QMenuBar, QAction, QInputDialog, QMessageBox, QProgressDialog, QApplication
from PyQt5.QtCore import Qt, QThread, pyqtSlot, pyqtSignal
import subprocess
import platform
from url_check_worker import URLCheckWorker
from about_dialog import AboutDialog
from url_utilities import getStreamURL, extractYouTubePlaylist, extractM3UUrls

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
        self.setFixedSize(400, 200)  # Para que no se pueda redimensionar la ventana
        
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
        
        playlist_action = QAction('Extraer URLs de lista en YouTube', self)
        playlist_action.triggered.connect(self.extractPlaylist)
        options_menu.addAction(playlist_action)
        
        m3u_action = QAction('Extraer URLs de un archivo .m3u', self)
        m3u_action.triggered.connect(self.extractM3U)
        options_menu.addAction(m3u_action)
        
        layout.setMenuBar(menubar)
        
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)
        
        button_layout = QHBoxLayout()
        self.check_button = QPushButton('Comprobar URL')
        self.check_button.setToolTip('Comprueba si la URL proporcionada está activa y es un archivo m3u8 o un flujo de transmisión multimedia')
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
        QApplication.processEvents()  # Fuerza la actualización de la interfaz de usuario

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

    def openInVLC(self):
        url = self.url_to_open
        stream_url = getStreamURL(url)
        if stream_url is None:
            QMessageBox.critical(self, "Error", "No se pudo obtener la URL de streaming.")
            return
        if not self.isVLCInstalled():
            QMessageBox.critical(self, "Error", "VLC no está instalado.")
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

    def extractPlaylist(self):
        playlist_url, ok = QInputDialog.getText(self, 'Extraer URLs de lista de YouTube', 'Ingrese la URL de la lista de YouTube:')
        if ok and playlist_url:
            progress_dialog = QProgressDialog("Extrayendo URLs...", "Cancelar", 0, 100, self)
            progress_dialog.setWindowTitle('Progreso de extracción')
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setMinimumDuration(0)

            self.result_label.setText('Preparando las URLs a reproducir...')
            self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: blue;")
            success = extractYouTubePlaylist(playlist_url, progress_dialog)
            if success:
                self.result_label.setText('URLs extraídas y guardadas en listas.txt')
                self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: green;")
                QMessageBox.information(self, 'Éxito', 'URLs extraídas y guardadas en el archivo listas.txt')
                self.openPlaylistInVLC()
            else:
                self.result_label.setText('No se encontraron entradas en la lista de reproducción')
                self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: red;")
                QMessageBox.critical(self, 'Error', 'No se pudieron extraer las URLs de la lista de reproducción o no se encontraron entradas.')

    def extractM3U(self):
        m3u_url, ok = QInputDialog.getText(self, 'Extraer URLs de archivo .m3u', 'Escribe la URL del archivo .m3u:')
        if ok and m3u_url:
            progress_dialog = QProgressDialog("Extrayendo URLs...", "Cancelar", 0, 100, self)
            progress_dialog.setWindowTitle('Progreso de extracción')
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setMinimumDuration(0)

            self.result_label.setText('Preparando las URLs a reproducir...')
            self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: blue;")
            success = extractM3UUrls(m3u_url, progress_dialog)
            if success:
                self.result_label.setText('URLs extraídas y guardadas en listas.txt')
                self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: green;")
                QMessageBox.information(self, 'Éxito', 'URLs extraídas y guardadas en listas.txt')
                self.openPlaylistInVLC()
            else:
                self.result_label.setText('No se encontraron URLs válidas en el archivo .m3u')
                self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: red;")
                QMessageBox.critical(self, 'Error', 'No se pudieron extraer URLs válidas del archivo .m3u.')

    def openPlaylistInVLC(self):
        try:
            with open('listas.txt', 'r') as file:
                urls = file.readlines()
            
            if not urls:
                QMessageBox.critical(self, "Error", "El archivo listas.txt está vacío o no contiene URLs válidas.")
                return

            urls = [url.strip() for url in urls if url.strip()]

            if not self.isVLCInstalled():
                QMessageBox.critical(self, "Error", "VLC no está instalado.")
                return

            vlc_command = ['vlc', '--playlist-enqueue'] + urls
            subprocess.Popen(vlc_command)
            
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "El archivo listas.txt no fue encontrado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fallo al abrir VLC: {str(e)}")

