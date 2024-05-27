import sys
from PyQt5.QtWidgets import QApplication
from url_checker import URLChecker


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = URLChecker()
    window.show()
    sys.exit(app.exec_())