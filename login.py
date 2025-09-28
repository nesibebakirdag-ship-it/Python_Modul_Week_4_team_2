from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)  # Başlangıç boyutu

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Ana layout
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.label_5 = QtWidgets.QLabel()
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_5.setFixedSize(120, 120)
        pixmap = QPixmap("./logo.png")
        pixmap = pixmap.scaled(self.label_5.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.label_5.setPixmap(pixmap)
        self.mainLayout.addWidget(self.label_5, alignment=Qt.AlignmentFlag.AlignCenter)



        formLayout = QtWidgets.QFormLayout()
        self.textEdit = QtWidgets.QLineEdit()  # QTextEdit yerine QLineEdit daha uygun
        self.textEdit_2 = QtWidgets.QLineEdit()
        self.textEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)  # Şifre gizleme
        formLayout.addRow("Username:", self.textEdit)
        formLayout.addRow("Password:", self.textEdit_2)
        self.mainLayout.addLayout(formLayout)

        # Login butonu
        self.pushButton = QtWidgets.QPushButton("Login")
        self.mainLayout.addWidget(self.pushButton, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Hata mesajı
        self.label_3 = QtWidgets.QLabel("Invalid email or password")
        self.label_3.setStyleSheet("color: red;")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.hide()  # Başta gizli
        self.mainLayout.addWidget(self.label_3)

        # Reset password
        self.label_4 = QtWidgets.QLabel("Reset password")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setStyleSheet("color: blue; text-decoration: underline;")
        self.mainLayout.addWidget(self.label_4)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        # Menü
        self.menuLogin_page = QtWidgets.QMenu("Login page", parent=self.menubar)
        self.menubar.addAction(self.menuLogin_page.menuAction())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
