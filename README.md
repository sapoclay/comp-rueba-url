## Comp-Rueba URL Versión 0.5

Un pequeño programa escrito con Python3 para comprobar listas de reproducción m3u8 o urls de streaming. El programa nos dirá si la URL pasada está activa o no, y de estar activa, nos permitirá reproducirla en VLC sin anuncios (en caso de los vídeos de Youtube ... ).

Añadida un opción para poder reproducir listas de youtube en VLC. Las url de las listas deben tomarse del canal de youtube, utilizando la opción disponible en el menú superior. Las listas que se extraigan se guardarán en la carpeta home del usuario, en un archivo llamado listas.txt. Las URL contenidas en las listas m3u, también se guardarán en este archivo. Archivo que debería ir sobreescribiendose tras cada uso. En caso de error se intentará la extracción de las listas de Youtube 3 veces antes de abortar.

En caso de que no tengas instalado VLC en tu equipo o alguna de las dependencias, deberían instalarse de forma automática. Aun que en Windows ffmpeg habrá que instalarlo manualmente.

Tanto las listas de Youtube como las listas m3u, tardarán más o menos, según la velocidad de respuesta por parte del servidor.

El programa cuenta con un log de errores en su directorio de instalación.

### A tener en cuenta

Según el servidor, es posible que al introducir una URL m3u8, la primera vez que solicite la comprobación aparezca la URL escrita como no disponible, pero si pulsas dos veces, puede funcionar.