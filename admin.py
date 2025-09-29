import sys
from PyQt6 import QtWidgets, uic

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi(r".\ui\admin.ui", self)  # .ui dosyasını yükler
        self.pushButton.clicked.connect(self.butonTiklandi)

    def butonTiklandi(self):
        print("Butona tıklandı!")

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())  # PyQt6 tarzı
