import requests
import yt_dlp

def isURLAvailable(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        print(f"Error al conectar a la URL: {str(e)}")
        return False

def getStreamURL(url):
    try:
        if "youtube.com" in url or "youtu.be" in url:
            ydl_opts = {
                'format': 'best',
                'quiet': True,
                'no_warnings': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info['url']
        return url  # Return the original URL for non-YouTube streams
    except Exception as e:
        print(f"Error al obtener la URL de streaming: {str(e)}")
        return None
