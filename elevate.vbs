'
'Este script VBScript (`elevate.vbs`) se utiliza para elevar los privilegios de un comando en Windows mediante el uso del Control de Cuentas de Usuario (UAC). 
'
'Funcionalidad:
'
'- El script crea una instancia del objeto `Shell.Application` para invocar el Control de Cuentas de Usuario (UAC).
'- Utiliza el método `ShellExecute` para ejecutar el comando proporcionado como argumento con privilegios elevados (modo administrador).
'- El comando se pasa a `cmd.exe` con el modificador `/c`, que ejecuta el comando y luego termina el proceso de la línea de comandos.

Set UAC = CreateObject("Shell.Application")
UAC.ShellExecute "cmd.exe", "/c " & WScript.Arguments(0), "", "runas", 1
