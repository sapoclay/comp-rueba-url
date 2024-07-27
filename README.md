## Comp-Rueba URL Versión 0.5.7

![about](https://github.com/user-attachments/assets/a6adc1b3-9e85-4760-b6d4-2456b31e8fd5)

* Escrito con: Python 3
* Este programa debería funcionar tanto en Windows como en Ubuntu, siempre que tengas instalado Python en el sistema en el que lo ejecutes. Se puede utilizar el código fuente o en Ubuntu se puede utilizar el paquete .DEB que está disponible en la página de lanzamientos de este repositorio.
### Consideraciones

![password](https://github.com/user-attachments/assets/fe7cfcc0-0f3c-47be-9561-ea386e9ac513)

Al iniciar el programa, se nos pedirá nuestra contraseña de usuario por si es necesario instalar alguna de las dependencias necesarias para que todo funcione como debe. Este programa se instalará en un entorno virtual que se creará de forma automática en el directorio en el que se instale el paquete .deb correspondiente.

![youtube-list](https://github.com/sapoclay/comp-rueba-url/assets/6242827/bb19dffc-48d6-44a6-9d53-880e0a075126)

Un pequeño programa escrito con Python para comprobar listas de reproducción .m3u (que contenga URL .m3u8) o urls de streaming (Por el momento solo Youtube). El programa nos dirá si la URL pasada está activa o no, y de estar activa, nos permitirá reproducirla en VLC sin anuncios (en caso de los vídeos de Youtube ... ). 

![busquedas-en-youtube](https://github.com/user-attachments/assets/3986ce3a-e300-4bdb-a432-ece2a6bc3b21)

También nos va permitir realizar búsquedas en Youtube y reproducir los vídeos o listas en VLC. Los resultados de las búsquedas todavía están por afinar.

![URL-no-disponible](https://github.com/sapoclay/comp-rueba-url/assets/6242827/fa15586c-ed28-40ab-9e1c-7e9d8a6f7f1e)

Las listas que se extraigan se guardarán en un archivo llamado lista.txt, el cual se va a encontrar en el mismo directorio en el que se instale el programa. 

![urls-m3u](https://github.com/user-attachments/assets/dabc62a9-53d9-4f66-a72a-ffc3f08c3852)

Las URL contenidas en las listas m3u, también se guardarán en este archivo. Archivo que debería ir sobreescribiendose tras cada uso. En caso de error se omitirá la URL que genera el error, y solo se guardarán en el archivo lista.txt las URL que estén funcionales en el momento el que se realice la comprobación.

En caso de que no tengas instalado VLC en tu equipo o alguna de las dependencias, deberían instalarse de forma automática. Aun que en Windows ffmpeg habrá que instalarlo manualmente.

Cuando se estraigan las URL de una lista m3u o de Youtube, podremos cerrar el programa, y en otro momento utilizando la opción disponible en la ventana principal, podremos cargar el archivo lista.txt directamente en VLC sin necesidad de volver a generar el archivo lista.txt.

Tanto las listas de Youtube como las listas m3u, tardarán más o menos en cargarse, según la velocidad de respuesta por parte del servidor y de nuestra conexión a internet.

El programa cuenta con un log de errores en su directorio de instalación. Desde la interfaz del programa podremos consultarlo o directamente eliminarlo (por que con el paso del tiempo irá cogiendo cierto tamaño)

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

En algunos sistemas quizás sea necesario eliminar también el directorio que contenía el programa:

``` sudo rm -rf /usr/share/Comp-Rueba ```
