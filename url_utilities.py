import requests
import yt_dlp
from PyQt5.QtWidgets import QProgressDialog

# Función para verificar si una URL está disponible
def isURLAvailable(url):
    try:
        # Realiza una solicitud GET a la URL con un tiempo de espera de 10 segundos
        response = requests.get(url, timeout=10)
        return response.status_code == 200  # Devuelve True si el código de estado es 200 (OK)
    except Exception as e:
        print(f"Error al conectar a la URL: {str(e)}")
        return False  # Devuelve False si ocurre una excepción

# Función para obtener la URL de streaming de una URL dada
def getStreamURL(url, retries=3, timeout=30):
    attempt = 0
    while attempt < retries:
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': 'best',
                'socket_timeout': timeout,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info['url'] if 'url' in info else info['entries'][0]['url']
        except yt_dlp.utils.DownloadError as e:
            print(f"Error al obtener la URL de streaming (Intento {attempt + 1}/{retries}): {str(e)}")
            if attempt == retries - 1:
                return None
            attempt += 1

# Función para extraer las URLs de una lista de reproducción de YouTube
def extractYouTubePlaylist(playlist_url, progress_dialog=None):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # Solo obtiene metadatos, no el contenido multimedia
            'force_generic_extractor': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            if 'entries' in info:
                urls = []
                total_entries = len(info['entries'])
                for idx, entry in enumerate(info['entries']):
                    # Actualiza la barra de progreso si existe
                    if progress_dialog:
                        progress_dialog.setValue(int((idx / total_entries) * 100))
                        if progress_dialog.wasCanceled():
                            return False
                    video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                    stream_url = getStreamURL(video_url)
                    if stream_url:
                        urls.append(stream_url)
                if urls:
                    # Guarda las URLs en un archivo 'listas.txt'
                    with open('listas.txt', 'w') as f:
                        f.write('\n'.join(urls))
                    if progress_dialog:
                        progress_dialog.setValue(100)
                    return True
                else:
                    print("No se pudieron obtener las URLs de transmisión.")
                    if progress_dialog:
                        progress_dialog.setValue(100)
                    return False
            else:
                print("No se encontraron entradas en la lista de reproducción.")
                if progress_dialog:
                    progress_dialog.setValue(100)
                return False
    except Exception as e:
        print(f"Error al extraer la lista de reproducción de YouTube: {str(e)}")
        if progress_dialog:
            progress_dialog.setValue(100)
        return False

# Función para extraer URLs de un archivo M3U
def extractM3UUrls(m3u_url, progress_dialog=None):
    try:
        # Realiza una solicitud GET a la URL del archivo M3U
        response = requests.get(m3u_url)
        response.raise_for_status()  # Lanza una excepción si la solicitud no es exitosa
        # Filtra las líneas del archivo M3U, ignorando las que comienzan con '#'
        urls = [line.strip() for line in response.text.splitlines() if line.strip() and not line.startswith("#")]
        
        valid_urls = []
        total_urls = len(urls)
        for idx, url in enumerate(urls):
            # Actualiza la barra de progreso si existe
            if progress_dialog:
                progress_dialog.setValue(int((idx / total_urls) * 100))
                if progress_dialog.wasCanceled():
                    return False
            if isURLAvailable(url):
                valid_urls.append(url)
        
        if valid_urls:
            # Guarda las URLs válidas en un archivo 'listas.txt'
            with open('listas.txt', 'w') as f:
                f.write('\n'.join(valid_urls))
            if progress_dialog:
                progress_dialog.setValue(100)
            return True
        else:
            print("No se pudieron obtener URLs válidas.")
            if progress_dialog:
                progress_dialog.setValue(100)
            return False
    except Exception as e:
        print(f"Error al extraer URLs de {m3u_url}: {str(e)}")
        if progress_dialog:
            progress_dialog.setValue(100)
        return False