from PyQt5.QtCore import QObject, pyqtSignal
import subprocess
import platform
import tempfile
import yt_dlp
import time

class URLCheckWorker(QObject):
    url_checked = pyqtSignal(bool)
    check_url_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.check_url_signal.connect(self.checkURL)

    def checkURL(self, url, retries=3, delay=5):
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