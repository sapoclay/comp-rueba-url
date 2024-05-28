import requests
import yt_dlp
from PyQt5.QtWidgets import QProgressDialog

def isURLAvailable(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Error al conectar a la URL: {str(e)}")
        return False

def getStreamURL(url):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url'] if 'url' in info else info['entries'][0]['url']
    except Exception as e:
        print(f"Error al obtener la URL de streaming: {str(e)}")
        return None

def extractYouTubePlaylist(playlist_url, progress_dialog=None):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # Ensures we only get metadata, not the actual media
            'force_generic_extractor': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            if 'entries' in info:
                urls = []
                total_entries = len(info['entries'])
                for idx, entry in enumerate(info['entries']):
                    if progress_dialog:
                        progress_dialog.setValue(int((idx / total_entries) * 100))
                        if progress_dialog.wasCanceled():
                            return False
                    video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                    stream_url = getStreamURL(video_url)
                    if stream_url:
                        urls.append(stream_url)
                if urls:
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
