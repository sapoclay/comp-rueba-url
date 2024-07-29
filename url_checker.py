import sys
import os
import subprocess
import platform
import webbrowser
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QMenuBar, QAction, QInputDialog, QMessageBox, QListWidget, QListWidgetItem, QApplication, QProgressDialog, QFileDialog, QMainWindow, QDialog
from PyQt5.QtCore import Qt, QThread, pyqtSlot, pyqtSignal
from url_check_worker import URLCheckWorker
import actualizaciones
from about_dialog import AboutDialog  
from url_utilities import extractYouTubePlaylist, extractM3UUrls
from youtubesearchpython import VideosSearch, PlaylistsSearch
import yt_dlp
from datetime import datetime  
from dateutil.parser import parse as parse_date
import tempfile

class URLChecker(QWidget):
    """
    URLChecker es una clase que representa una aplicación de PyQt5 para verificar la disponibilidad de URLs,
    extraer URLs de listas de reproducción de YouTube y archivos M3U, y abrir URLs en VLC Media Player.
    """
    def __init__(self):
        """
        Inicializa una instancia de la clase URLChecker.
        """
        super().__init__()
        self.initUI()
        self.url_check_thread = QThread()
        self.url_check_worker = URLCheckWorker()
        self.url_check_worker.moveToThread(self.url_check_thread)
        self.url_check_worker.url_checked.connect(self.handleURLChecked)
        self.url_check_thread.start()
        self.results_window = None

    @pyqtSlot(bool)
    def handleURLChecked(self, is_available):
        """
        Maneja la señal de verificación de URL y actualiza la interfaz de usuario en consecuencia.

        Argumentos:
            is_available (bool): Indica si la URL está disponible o no.
        """
        if is_available:
            self.result_label.setText('URL activa')
            self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: green;")
            self.open_vlc_button.setVisible(True)
            self.url_to_open = self.url_input.text().strip()
        else:
            self.result_label.setText('URL no disponible')
            self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: red;")
            self.open_vlc_button.setVisible(False)

    def abrir_url_github(self):
        """
        Abre la URL del repositorio de GitHub en el navegador web predeterminado.
        """
        webbrowser.open("https://github.com/sapoclay/comp-rueba-url")
        
    def abrir_vpn(self):
        """
        Abre la URL para obtener una VPN gratuita durante 30 días en el navegador web predeterminado.
        """
        webbrowser.open("https://www.expressvpn.com/refer-a-friend/30-days-free?locale=es&referrer_id=40141467&utm_campaign=referrals&utm_medium=copy_link&utm_source=referral_dashboard")

    def showAboutDialog(self):
        """
        Muestra el cuadro de diálogo "About" de la aplicación.
        """
        dialog = AboutDialog(self)
        dialog.exec_()
    
    def abrir_ventana_actualizaciones(self):
        """
        Abre la ventana de actualizaciones, si ocurre un error muestra un mensaje crítico.
        """
        try:
            ventana_actualizaciones = actualizaciones.VentanaActualizaciones()
            ventana_actualizaciones.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir ventana de actualizaciones: {str(e)}")

    def abrir_archivo_log(self):
        """
        Abre el archivo de registro en el sistema operativo predeterminado.
        """
        try:
            temp_dir = tempfile.gettempdir()
            logfile_path = os.path.join(temp_dir, 'registro.log')
            if os.path.exists(logfile_path):
                if platform.system() == 'Windows':
                    os.startfile(logfile_path)
                elif platform.system() == 'Darwin':
                    subprocess.Popen(['open', logfile_path])
                elif platform.system() == 'Linux':
                    subprocess.Popen(['xdg-open', logfile_path])
                else:
                    raise Exception('Plataforma no compatible')
            else:
                QMessageBox.warning(self, "Archivo no encontrado", "El archivo de registro.log no se encuentra.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir el archivo de registro.log: {str(e)}")

    def eliminar_archivo_log(self):
        """
        Elimina el archivo de registro del sistema operativo.
        """
        try:
            temp_dir = tempfile.gettempdir()
            logfile_path = os.path.join(temp_dir, 'registro.log')
            if os.path.exists(logfile_path):
                os.remove(logfile_path)
                QMessageBox.information(self, "Archivo eliminado", "El archivo de registro.log ha sido eliminado.")
            else:
                QMessageBox.warning(self, "Archivo no encontrado", "El archivo de registro.log no se encuentra.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar el archivo de registro.log: {str(e)}")

    def initUI(self):
        """
        Inicializa la interfaz de usuario de la aplicación.
        """
        self.setWindowTitle('Comp-Rueba-URL')
        self.setGeometry(100, 100, 400, 200)
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        menubar = QMenuBar(self)

        file_menu = menubar.addMenu('Archivo')
        vpn_action = QAction('VPN Gratis 30 días', self)
        vpn_action.triggered.connect(self.abrir_vpn)
        file_menu.addAction(vpn_action)
        exit_action = QAction('Salir', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        options_menu = menubar.addMenu('Opciones')
        actualizacion_action = QAction('Buscar Actualización', self)
        actualizacion_action.triggered.connect(self.abrir_ventana_actualizaciones)
        options_menu.addAction(actualizacion_action)
        playlist_action = QAction('Extraer URLs de lista en YouTube', self)
        playlist_action.triggered.connect(self.extractPlaylist)
        options_menu.addAction(playlist_action)
        m3u_action = QAction('Extraer URLs de una lista .m3u', self)
        m3u_action.triggered.connect(self.extractM3U)
        options_menu.addAction(m3u_action)
        load_list_action = QAction('Cargar lista de canales en VLC', self)
        load_list_action.triggered.connect(self.loadListInVLC)
        options_menu.addAction(load_list_action)
        
        view_menu = menubar.addMenu('Log')
        open_log_action = QAction('Abrir registro.log', self)
        open_log_action.triggered.connect(self.abrir_archivo_log)
        view_menu.addAction(open_log_action)
        delete_log_action = QAction('Eliminar registro.log', self)
        delete_log_action.triggered.connect(self.eliminar_archivo_log)
        view_menu.addAction(delete_log_action)

        about_menu = menubar.addMenu('About')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.showAboutDialog)
        about_menu.addAction(about_action)
        github_action = QAction('Repositorio', self)
        github_action.triggered.connect(self.abrir_url_github)
        about_menu.addAction(github_action)

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

        self.youtube_search_button = QPushButton('Buscar en YouTube')
        self.youtube_search_button.setToolTip('Buscar videos y listas de reproducción en YouTube')
        self.youtube_search_button.clicked.connect(self.openYoutubeSearch)
        button_layout.addWidget(self.youtube_search_button)

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
        """
        Comprueba la URL proporcionada para verificar si está activa y es un archivo m3u8 o un flujo de transmisión multimedia.
        """
        url = self.url_input.text().strip()
        self.url_input.setText(url)
        self.result_label.setText('Verificando URL...')
        self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: blue;")
        QApplication.processEvents()
        self.url_check_worker.check_url_signal.emit(url)

    def clearURL(self):
        """
        Borra el contenido del campo de entrada de URL.
        """
        self.url_input.clear()
        self.result_label.clear()
        self.open_vlc_button.setVisible(False)

    def openInVLC(self):
        try:
            if not self.isVLCInstalled():
                QMessageBox.critical(self, "Error", "VLC no está instalado en el sistema. Por favor, instale VLC y vuelva a intentarlo.")
                return

            url = self.url_input.text().strip()
            if 'youtube.com' in url or 'youtu.be' in url:
                stream_url = get_stream_url(url)
            else:
                stream_url = self.url_to_open

            if platform.system() == 'Windows':
                command = ['vlc', '--play-and-exit', stream_url]
            elif platform.system() == 'Darwin':
                command = ['/Applications/VLC.app/Contents/MacOS/VLC', '--play-and-exit', stream_url]
            elif platform.system() == 'Linux':
                command = ['vlc', '--play-and-exit', stream_url]
            else:
                raise Exception('Plataforma no compatible')

            subprocess.Popen(command)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir VLC: {str(e)}")
            
    def loadListInVLC(self):
        """
        Carga una lista de canales en VLC Media Player desde un archivo seleccionado por el usuario.
        """
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lista.txt')
        if os.path.exists(file_path):
            self.openURLsInVLC(file_path)
        else:
            QMessageBox.critical(self, "Error", "El archivo con la lista de canales no se ha generado. Utiliza primero la opción 'Extraer URL's de una lista .m3u'.")


    def closeEvent(self, event):
        """
        Muestra un mensaje para a la hora de cerrar el programa.
        """
        reply = QMessageBox.question(self, 'Confirmar salida', '¿Está seguro de que desea cerrar la aplicación?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def isVLCInstalled(self):
        """
        Comprueba si VLC está instalado, según el sistema operativo en el que se ejecute el programa.
        """
        try:
            if platform.system() == 'Windows':
                subprocess.call(['vlc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif platform.system() == 'Darwin':
                subprocess.call(['/Applications/VLC.app/Contents/MacOS/VLC', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif platform.system() == 'Linux':
                subprocess.call(['vlc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                return False
            return True
        except FileNotFoundError:
            return False

    def openYoutubeSearch(self):
        if self.results_window is None:
            self.results_window = YoutubeSearchWindow(self)
        self.results_window.show()

    def extractPlaylist(self):
        """
        Extrae URLs de una lista de reproducción de YouTube y las muestra en un cuadro de diálogo.
        """
        url, ok = QInputDialog.getText(self, 'Extraer URLs de lista de YouTube', 'Introduce la URL de la lista de reproducción de YouTube:')
        if ok and url:
            self.extractAndOpenPlaylistInVLC(url)


    def extractM3U(self):
        """
        Extrae URLs de un archivo M3U seleccionado por el usuario y las muestra en un cuadro de diálogo.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, 'Seleccionar archivo .m3u', '', 'Archivos .m3u (*.m3u);;Archivos .m3u8 (*.m3u8)')
        if file_path:
            progress_dialog = QProgressDialog("Extrayendo URLs...", "Cancelar", 0, 100, self)
            progress_dialog.setWindowTitle('Progreso de extracción')
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setMinimumDuration(0)

            self.result_label.setText('Preparando las URLs a reproducir...')
            self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: blue;")
            success = extractM3UUrls(file_path, progress_dialog)
            if success:
                self.result_label.setText('URLs guardadas. Abriendo archivo en VLC')
                self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: green;")
                QMessageBox.information(self, 'Éxito', 'URLs extraídas y guardadas en lista.txt')
                self.openURLsInVLC()
            else:
                self.result_label.setText('No se encontraron URLs válidas en el archivo .m3u')
                self.result_label.setStyleSheet("font-weight: bold; font-size: 16px; color: red;")
                QMessageBox.critical(self, 'Error', 'No se pudieron extraer URLs válidas del archivo .m3u.')

    def extractAndOpenPlaylistInVLC(self, url):
        progress_dialog = QProgressDialog("Extrayendo URLs de la lista de reproducción...", "Cancelar", 0, 100, self)
        progress_dialog.setWindowTitle("Progreso")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        urls = extractYouTubePlaylist(url, progress_dialog)
        if urls:
            self.saveURLsToFile(urls)
            self.openURLsInVLC()
        else:
            QMessageBox.critical(self, "Error", "No se encontraron URLs en la lista de reproducción proporcionada.")

    def saveURLsToFile(self, urls):
        try:
            if not isinstance(urls, list):
                raise Exception("La entrada proporcionada no es una lista de URLs.")
            
            # Obtener el directorio de instalación del programa
            install_dir = os.path.dirname(os.path.realpath(__file__))
            print(f"Directorio de instalación del programa: {install_dir}")  # Añadido para depuración
            lista_path = os.path.join(install_dir, 'lista.txt')
            print(f"Ruta de archivo lista.txt: {lista_path}")  # Añadido para depuración
            
            progress_dialog = QProgressDialog("Guardando URLs...", "Cancelar", 0, len(urls), self)
            progress_dialog.setWindowTitle("Progreso")
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setValue(0)
            progress_dialog.show()

            with open(lista_path, 'w') as file:
                for i, url in enumerate(urls):
                    file.write(url + '\n')
                    progress_dialog.setValue(i + 1)
                    if progress_dialog.wasCanceled():
                        break
            
            progress_dialog.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar las URLs en lista.txt: {str(e)}")

    def openURLsInVLC(self, file_path='lista.txt'):
        try:
            if not self.isVLCInstalled():
                QMessageBox.critical(self, "Error", "VLC no está instalado en el sistema. Por favor, instale VLC y vuelva a intentarlo.")
                return

            file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lista.txt')
            print(f"Ruta de archivo lista.txt para VLC: {file_path}")  # Añadido para depuración

            if platform.system() == 'Windows':
                command = ['vlc', '--playlist-enqueue', '--no-video-title-show', '--network-caching=1000', '--ts-seek-percent', '--sout-ts-dts-delay=400', file_path]
            elif platform.system() == 'Darwin':
                command = ['/Applications/VLC.app/Contents/MacOS/VLC', '--playlist-enqueue', '--no-video-title-show', '--network-caching=1000', '--ts-seek-percent', '--sout-ts-dts-delay=400', file_path]
            elif platform.system() == 'Linux':
                command = ['vlc', '--playlist-enqueue', '--no-video-title-show', '--network-caching=1000', '--ts-seek-percent', '--sout-ts-dts-delay=400', file_path]
            else:
                raise Exception('Plataforma no compatible')

            subprocess.Popen(command)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir VLC con las URLs de la lista: {str(e)}")



class YoutubeSearchWindow(QDialog):
    """
    YoutubeSearchWindow es una clase que representa una ventana de diálogo de PyQt5 para buscar videos y listas de reproducción en YouTube.

    Atributos:
        search_input (QLineEdit): Campo de entrada para el término de búsqueda.
        results_list (QListWidget): Lista para mostrar los resultados de la búsqueda.

    Métodos:
        __init__(self, parent=None): Inicializa la instancia de la clase.
        searchYouTube(self): Realiza la búsqueda en YouTube y muestra los resultados.
        paginatedSearch(self, searchClass, query, max_results): Realiza una búsqueda paginada en YouTube.
        parse_time(self, time_str): Analiza una cadena de tiempo y la convierte en un objeto datetime.
        itemDoubleClicked(self, item): Maneja el evento de doble clic en un elemento de la lista de resultados.
        showNoResultsMessage(self, query): Muestra un mensaje de información cuando no se encuentran resultados.
        closeEvent(self, event): Maneja el evento de cierre de la ventana.
    """
    def __init__(self, parent=None):
        """
        Inicializa una instancia de la clase YoutubeSearchWindow.

        Argumentos:
            parent (QWidget, opcional): El widget padre de esta ventana de diálogo. Por defecto es None.
        """
        super().__init__(parent)
        self.setWindowTitle('Buscar en YouTube')
        self.setGeometry(150, 150, 500, 400)
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        layout.addWidget(self.search_input)

        search_button = QPushButton('Buscar', self)
        search_button.clicked.connect(self.searchYouTube)
        layout.addWidget(search_button)

        self.results_list = QListWidget(self)
        self.results_list.itemDoubleClicked.connect(self.itemDoubleClicked)
        layout.addWidget(self.results_list)

        self.setLayout(layout)

    def searchYouTube(self):
        """
        Realiza una búsqueda en YouTube y muestra los resultados en la lista de resultados.
        """
        query = self.search_input.text().strip()
        if query:
            self.results_list.clear()

            # Buscar videos
            videos_results = self.paginatedSearch(VideosSearch, query, 60)
            if not videos_results:
                self.showNoResultsMessage(query)
                return
            videos_results.sort(
                key=lambda x: self.parse_time(x.get('publishedTime')), reverse=True
            )
            videos_divider = QListWidgetItem('----- Videos -----')
            videos_divider.setBackground(Qt.lightGray)
            self.results_list.addItem(videos_divider)
            for result in videos_results:
                duration = result.get('duration', 'N/A')
                item = QListWidgetItem(f"{result['title']} ({duration})")
                item.setData(Qt.UserRole, result['link'])
                self.results_list.addItem(item)

            # Buscar listas de reproducción
            playlists_results = self.paginatedSearch(PlaylistsSearch, query, 60)
            if not playlists_results:
                self.showNoResultsMessage(query)
                return
            playlists_divider = QListWidgetItem('----- Listas de reproducción -----')
            playlists_divider.setBackground(Qt.lightGray)
            self.results_list.addItem(playlists_divider)
            for result in playlists_results:
                item_count = result['videoCount']
                item = QListWidgetItem(f"{result['title']} ({item_count} videos)")
                item.setData(Qt.UserRole, result['link'])
                self.results_list.addItem(item)

    def paginatedSearch(self, searchClass, query, max_results):
        """
        Realiza una búsqueda paginada en YouTube utilizando la clase de búsqueda especificada.

        Argumentos:
            searchClass (class): Clase de búsqueda a utilizar (VideosSearch o PlaylistsSearch).
            query (str): Término de búsqueda.
            max_results (int): Número máximo de resultados a obtener.

        Devuelve:
            list: Lista de resultados de la búsqueda.
        """
        all_results = []
        search_instance = searchClass(query, limit=20)
        next_page = search_instance.result().get('nextPageToken')
        all_results.extend(search_instance.result().get('result', []))

        while next_page and len(all_results) < max_results:
            search_instance = searchClass(query, limit=20, token=next_page)
            next_page = search_instance.result().get('nextPageToken')
            all_results.extend(search_instance.result().get('result', []))
        
        return all_results[:max_results]

    def parse_time(self, time_str):
        """
        Analiza una cadena de tiempo y la convierte en un objeto datetime.

        Argumentos:
            time_str (str): Cadena de tiempo a analizar.

        Devuelve:
            datetime: Objeto datetime correspondiente a la cadena de tiempo analizada.
        """
        if not time_str:
            return datetime(1970, 1, 1)
        try:
            return parse_date(time_str)
        except ValueError:
            return datetime(1970, 1, 1)

    def itemDoubleClicked(self, item):
        """
        Maneja el evento de doble clic en un elemento de la lista de resultados.

        Argumentos:
            item (QListWidgetItem): Elemento de la lista de resultados que fue doble clickeado.
        """
        url = item.data(Qt.UserRole)
        if url:
            if 'playlist' in url:
                self.parent().extractAndOpenPlaylistInVLC(url)
            else:
                self.parent().url_input.setText(url)
                self.close()

    def showNoResultsMessage(self, query):
        """
        Muestra un mensaje de información cuando no se encuentran resultados para la búsqueda.

        Argumentos:
            query (str): Término de búsqueda que no produjo resultados.
        """
        QMessageBox.information(self, 'Sin Resultados', f'No se encontraron resultados para "{query}".', QMessageBox.Ok)

    def closeEvent(self, event):
        """
        Maneja el evento de cierre de la ventana.

        Argumentos:
            event (QCloseEvent): Evento de cierre.
        """
        self.close()

def get_stream_url(url):
    """
    Obtiene la URL del flujo de video de un video de YouTube utilizando yt_dlp.

    Argumentos:
        url (str): La URL del video de YouTube.

    Devuelve:
        str: La URL del flujo de video.
    """
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict['url']

if __name__ == '__main__':
    """
    Punto de entrada principal de la aplicación.

    Crea y muestra la ventana principal de la aplicación URLChecker.
    """
    app = QApplication(sys.argv)
    window = URLChecker()
    window.show()
    sys.exit(app.exec_())