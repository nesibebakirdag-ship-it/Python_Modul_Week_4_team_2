from PyQt6 import QtWidgets
import sys
from Interviews import Ui_MainWindow  # pyuic6 çıktısı

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # burası çok önemli! Arayüz öğelerini buraya yerleştirir


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
