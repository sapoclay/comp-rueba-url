## Comp-Rueba URL Versión 0.5

![youtube-list](https://github.com/sapoclay/comp-rueba-url/assets/6242827/bb19dffc-48d6-44a6-9d53-880e0a075126)

Un pequeño programa escrito con Python 3.10 para comprobar listas de reproducción m3u8 o urls de streaming. El programa nos dirá si la URL pasada está activa o no, y de estar activa, nos permitirá reproducirla en VLC sin anuncios (en caso de los vídeos de Youtube ... ).

![URL-no-disponible](https://github.com/sapoclay/comp-rueba-url/assets/6242827/fa15586c-ed28-40ab-9e1c-7e9d8a6f7f1e)

Añadida un opción para poder reproducir listas de youtube en VLC. Las url de las listas deben tomarse del canal de youtube, y pegarlas en la opción disponible en el menú superior del programa. Las listas que se extraigan se guardarán en la carpeta home del usuario, en un archivo llamado listas.txt. Las URL contenidas en las listas m3u, también se guardarán en este archivo. Archivo que debería ir sobreescribiendose tras cada uso. En caso de error se intentará la extracción de las listas de Youtube 3 veces antes de abortar.

El archivo listas.txt se va a borrar cuando cerremos el programa.

En caso de que no tengas instalado VLC en tu equipo o alguna de las dependencias, deberían instalarse de forma automática. Aun que en Windows ffmpeg habrá que instalarlo manualmente.

Tanto las listas de Youtube como las listas m3u, tardarán más o menos en cargarse, según la velocidad de respuesta por parte del servidor y de nuestra conexión a internet.

El programa cuenta con un log de errores en su directorio de instalación.

### A tener en cuenta

Es imprescindible tener instalado Python 3.10 (que es con el que yo desarrollé este código) para que funcione.

Según el servidor que aloje la URL m3u8, es posible que la primera vez que solicite la comprobación aparezca la URL escrita como no disponible, pero si pulsas dos veces, puede funcionar. La respuesta, tardará más o menos en función del tiepo de respuesta del servidor.

## Instalar paquete .DEB

![etb-reproduciendo](https://github.com/sapoclay/comp-rueba-url/assets/6242827/642b25b7-70fb-49e2-bdd4-f313007d9eda)

Para instalar el paquete .DEB, basta con descargarlo de la URL: https://github.com/sapoclay/comp-rueba-url/releases

Una vez que lo tengamos en nuestro equipo, en una terminal (Ctrl+Alt+T), basta con escribir desde la carpeta en la que tengamos guardado el paquete .DEB:

``` sudo dpkg -i Comp-Rueba-URL.deb ```

Terminada la instalación, solo queda buscar el lanzador del programa en nuestro equipo:

![lanzador](https://github.com/sapoclay/comp-rueba-url/assets/6242827/78bd91af-3798-4051-819f-de9c22544409)

### Desinstalar .DEB

En Ubuntu ... y cosas parecidas, en una terminal (Ctrl+Alt+T), solo tendremos que ejecutar el comando:

``` sudo apt remove comp-rueba-url ```
