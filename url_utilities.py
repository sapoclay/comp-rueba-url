import requests
from yt_dlp import YoutubeDL
from PyQt5.QtWidgets import QProgressDialog
import os


# Función para verificar si una URL está disponible con tiempo de espera y manejo de excepciones
def isURLAvailable(url, timeout=10):
    """
    Verifica si una URL está disponible.

    Parámetros:
        url (str): La URL a verificar.
        timeout (int, optional): Tiempo de espera para la solicitud en segundos. Por defecto es 10 segundos.

    Devuelve:
        bool: True si la URL está disponible (código de estado 200), False en caso contrario.
    """
    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error al verificar URL {url}: {str(e)}")
        return False

    
# Función para obtener la URL de streaming de una URL dada
def getStreamURL(url):
    """
    Obtiene la URL de streaming de una URL dada.

    Parámetros:
        url (str): La URL de la cual se quiere obtener el streaming.

    Devuelve:
        str: La URL de streaming.
    """
    ydl_opts = {'format': 'best', 'quiet': True, 'noplaylist': True}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict['url']

# Función para extraer las URL de una lista de Youtube
def extractYouTubePlaylist(playlist_url, progress_dialog=None):
    """
    Extrae las URLs de streaming de una lista de reproducción de YouTube.

    Parámetros:
        playlist_url (str): La URL de la lista de reproducción de YouTube.
        progress_dialog (QProgressDialog, optional): Un diálogo de progreso para actualizar mientras se extraen las URLs.

    Devuelve:
        list: Una lista de URLs de streaming de los videos en la lista de reproducción.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True
    }
    urls = []
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)
        total_videos = len(info_dict['entries'])
        
        if progress_dialog:
            progress_dialog.setMaximum(total_videos)
        
        for i, video in enumerate(info_dict['entries']):
            if progress_dialog:
                progress_dialog.setValue(i + 1)
                if progress_dialog.wasCanceled():
                    break
            video_url = video['url']
            stream_url = getStreamURL(video_url)
            urls.append(stream_url)
    
    if progress_dialog:
        progress_dialog.setValue(total_videos)
        progress_dialog.close()
    
    return urls

# Función para extraer las URL válidas de un listado m3u
def extractM3UUrls(file_path, progress_dialog=None):
    """
    Extrae URLs válidas de un archivo M3U.

    Parámetros:
        file_path (str): La ruta del archivo M3U.
        progress_dialog (QProgressDialog, optional): Un diálogo de progreso para actualizar mientras se extraen las URLs.

    Devuelve:
        bool: True si se encontraron y guardaron URLs válidas, False en caso contrario.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        urls = [line.strip() for line in lines if line.strip() and line.strip().startswith('http')]
        
        valid_urls = []
        total_urls = len(urls)
        for idx, url in enumerate(urls):
            if progress_dialog:
                progress_dialog.setValue(int((idx / total_urls) * 100))
                if progress_dialog.wasCanceled():
                    return False
            print(f"Verificando URL: {url}")  # Línea de depuración
            if isURLAvailable(url):
                valid_urls.append(url)
            else:
                print(f"URL no disponible: {url}")
        # Obtener el directorio de instalación del programa
        install_dir = os.path.dirname(os.path.realpath(__file__))
        lista_path = os.path.join(install_dir, 'lista.txt')
         
        if valid_urls:
            with open(lista_path, 'w') as f:
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
        print(f"Error al extraer URLs del archivo {file_path}: {str(e)}")
        if progress_dialog:
            progress_dialog.setValue(100)
        return False
