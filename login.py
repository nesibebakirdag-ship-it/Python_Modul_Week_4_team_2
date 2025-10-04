from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
import threading
import requests
from ErrorTypeEnum import  ErrorType, ERROR_MAP, ERROR_TEXT


class Ui_MainWindow(QtWidgets.QMainWindow):
    login_finished = pyqtSignal(object,str)

    def __init__(self):
        super().__init__()
        self.setupUi()
        self.login_finished.connect(self.on_login_result)

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(400, 300)

        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.setCentralWidget(self.centralwidget)

        # Ana layout
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Logo
        self.label_5 = QtWidgets.QLabel()
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_5.setFixedSize(120, 120)
        pixmap = QPixmap("./img/logo.png")
        pixmap = pixmap.scaled(self.label_5.size(), Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        self.label_5.setPixmap(pixmap)
        self.mainLayout.addWidget(self.label_5, alignment=Qt.AlignmentFlag.AlignCenter)

        # Form
        formLayout = QtWidgets.QFormLayout()
        self.username = QtWidgets.QLineEdit()
        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        formLayout.addRow("Username:", self.username)
        formLayout.addRow("Password:", self.password)
        self.mainLayout.addLayout(formLayout)

        # Login butonu
        self.pushButton = QtWidgets.QPushButton("Login")
        self.mainLayout.addWidget(self.pushButton, alignment=Qt.AlignmentFlag.AlignCenter)
        self.pushButton.clicked.connect(self.loginbttn)

        # Hata mesajı QLabel
        self.label_3 = QtWidgets.QLabel("")
        self.label_3.setStyleSheet("color: red;")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3.hide()
        self.mainLayout.addWidget(self.label_3)

        # Reset password
        self.label_4 = QtWidgets.QLabel("Reset password")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4.setStyleSheet("color: blue; text-decoration: underline;")
        self.mainLayout.addWidget(self.label_4)

        # Menü ve status bar (opsiyonel)
        self.menubar = QtWidgets.QMenuBar(parent=self)
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=self)
        self.setStatusBar(self.statusbar)

    def loginbttn(self):
        username = self.username.text()
        password = self.password.text()
        self.label_3.hide()

        # Boş alan kontrolü
        if username == "" or password == "":
            self.error_login(ErrorType.EMPTY)
            return

        # Butonu disable et ve durum yaz
        self.pushButton.setEnabled(False)
        self.pushButton.setText("Gönderiliyor...")

        # Thread ile HTTP isteği
        threading.Thread(target=self.send_request, args=(username, password), daemon=True).start()

    def send_request(self, username, password):
        url = "http://127.0.0.1:8000/login"
        try:
            data = None
            resp = requests.post(url, json={"username": username, "password": password}, timeout=8)
            data = resp.json()

            if resp.status_code == 200:
                self.login_finished.emit(data,None)
            else:
                self.login_finished.emit(None,data["detail"])

        except Exception as e:
            self.login_finished.emit(None,str(e))


        # GUI thread’ine signal ile gönder

    def error_login(self, errorType):
        self.label_3.setText(ERROR_TEXT.get(errorType, "There is a problem"))
        self.label_3.show()

    def on_login_result(self, data: dict,error: object):
        self.pushButton.setEnabled(True)
        self.pushButton.setText("Login")
    
        if data is not None:
            QtWidgets.QMessageBox.information(self, "Succes" , "Succes login: "+ data["kullanici"])

            self.label_3.hide()  # Başarılı ise hata mesajını gizle
        else:
            error_type = ERROR_MAP.get(error, ErrorType.OTHER)
            self.error_login(error_type)


