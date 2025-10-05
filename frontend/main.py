import sys
from PyQt6 import QtWidgets

from page.Login import Ui_MainWindow  # absolute import

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec())
