import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from views.app import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setWindowIcon(QIcon("./favicon.ico"))
    main_window.show()
    sys.exit(app.exec_())

