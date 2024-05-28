# Importar la función de verificación de dependencias
from dependencias import ensure_all_dependencies

# Verificar e instalar todas las dependencias necesarias
ensure_all_dependencies()

# El resto de tu código principal aquí
# ...

import sys
from PyQt5.QtWidgets import QApplication
from url_checker import URLChecker

if __name__ == "__main__":
    app = QApplication(sys.argv)
    url_checker = URLChecker()
    url_checker.show()
    sys.exit(app.exec_())