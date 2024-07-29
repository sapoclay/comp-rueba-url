from PyQt5.QtCore import QObject, pyqtSignal
import subprocess
import platform
import tempfile
import yt_dlp
import time
 
class URLCheckWorker(QObject):
    """
    Clase que se encarga de verificar la validez de URLs, tanto de YouTube como generales, utilizando
    yt_dlp y VLC respectivamente. La clase emite señales indicando el resultado de la verificación.

    Atributos:
        url_checked (pyqtSignal): Señal emitida cuando la URL ha sido verificada, con un valor booleano indicando éxito o fallo.
        check_url_signal (pyqtSignal): Señal utilizada para iniciar la verificación de una URL.

    Métodos:
        __init__(): Inicializa la instancia y conecta la señal check_url_signal al método checkURL.
        checkURL(url, retries=3, delay=5): Verifica la URL proporcionada, reintentando en caso de fallo.
        checkYouTubeURL(url): Verifica si una URL de YouTube es válida utilizando yt_dlp.
        checkGeneralURL(url): Verifica si una URL general es válida utilizando VLC.
    """
    url_checked = pyqtSignal(bool)
    check_url_signal = pyqtSignal(str)

    def __init__(self):
        """Inicializa la instancia de URLCheckWorker y conecta la señal check_url_signal al método checkURL."""
        super().__init__()
        self.check_url_signal.connect(self.checkURL)

    def checkURL(self, url, retries=3, delay=5):
        """
        Verifica la URL proporcionada, reintentando en caso de fallo.

        Argumentos:
            url (str): La URL a verificar.
            retries (int): Número de intentos de verificación en caso de fallo. Por defecto es 3.
            delay (int): Tiempo de espera en segundos entre reintentos. Por defecto es 5.
        """
        success = False
        for attempt in range(retries):
            if "youtube.com" in url or "youtu.be" in url:
                success = self.checkYouTubeURL(url)
            else:
                success = self.checkGeneralURL(url)
            
            if success:
                self.url_checked.emit(True)
                return
            
            print(f"Intento {attempt + 1} fallido, reintentando en {delay} segundos...")
            time.sleep(delay)
        
        self.url_checked.emit(False)

    def checkYouTubeURL(self, url):
        """
        Verifica si una URL de YouTube es válida utilizando yt_dlp.

        Args:
            url (str): La URL de YouTube a verificar.

        Returns:
            bool: True si la URL es válida, False en caso contrario.
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': 'best',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_url = info_dict.get("url", None)
                if video_url:
                    return True
                else:
                    return False
        except Exception as e:
            print(f"Error al verificar la URL de YouTube: {e}")
            return False

    def checkGeneralURL(self, url):
        """
        Verifica si una URL general es válida utilizando VLC.

        Args:
            url (str): La URL general a verificar.

        Returns:
            bool: True si la URL es válida, False en caso contrario.
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                log_file = temp_file.name

            if platform.system() == 'Windows':
                vlc_command = ['vlc', '--intf', 'dummy', '--no-video-title-show', '--no-audio', '--no-video', '--play-and-exit', '--run-time=1', url, '>', log_file, '2>&1']
            elif platform.system() == 'Darwin':
                vlc_command = ['/Applications/VLC.app/Contents/MacOS/VLC', '--intf', 'dummy', '--no-video-title-show', '--no-audio', '--no-video', '--play-and-exit', '--run-time=1', url, '>', log_file, '2>&1']
            elif platform.system() == 'Linux':
                vlc_command = ['cvlc', '--no-video-title-show', '--no-audio', '--no-video', '--play-and-exit', '--run-time=1', url, '>', log_file, '2>&1']

            result = subprocess.run(" ".join(vlc_command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            with open(log_file, 'r') as file:
                output = file.read()

            print(output)

            error_messages = [
                "access error", "Your input can't be opened",
                "unable to open", "Could not connect", "Failed to open",
                "Network is unreachable", "Connection refused", "http stream error",
                "access stream error", "main stream error"
            ]

            is_valid = not any(error_message in output for error_message in error_messages)
            return is_valid
        except Exception as e:
            print(f"Error al verificar la URL con VLC: {e}")
            return False