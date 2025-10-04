from PyQt6 import QtCore, QtGui, QtWidgets,uic
from PyQt6.QtWidgets import QTableWidgetItem
import requests
import sys
from base_window import BaseWindow


class Interviews(BaseWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.send_request()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 0, 781, 561))
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        # Logo
        self.logo = QtWidgets.QLabel(parent=self.frame)
        self.logo.setGeometry(QtCore.QRect(100, 30, 271, 71))
        self.logo.setPixmap(QtGui.QPixmap("logo1.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")

        # Labels
        self.interviews = QtWidgets.QLabel(parent=self.frame)
        self.interviews.setGeometry(QtCore.QRect(390, 40, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(29)
        font.setBold(True)
        font.setWeight(75)
        self.interviews.setFont(font)
        self.interviews.setObjectName("interviews")

        self.menu = QtWidgets.QLabel(parent=self.frame)
        self.menu.setGeometry(QtCore.QRect(320, 100, 221, 41))
        self.menu.setFont(font)
        self.menu.setObjectName("menu")

        # Search LineEdit
        self.linesearch = QtWidgets.QLineEdit(parent=self.frame)
        self.linesearch.setGeometry(QtCore.QRect(50, 220, 113, 20))
        self.linesearch.setStyleSheet("background-color: rgb(207, 207, 207);")
        self.linesearch.setObjectName("linesearch")

        # Buttons
        self.bttnsearch = QtWidgets.QPushButton(parent=self.frame)
        self.bttnsearch.setGeometry(QtCore.QRect(50, 280, 111, 23))
        self.bttnsearch.setText("Search")
        self.bttnsearch.setObjectName("bttnsearch")
        self.bttnsearch.clicked.connect(self.search_button)

        #gonderilmis projeler buton
        self.pushButton = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton.setGeometry(QtCore.QRect(50, 350, 111, 23))
        self.pushButton.setText("Submitted Projects")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.submitted_project_bttn)

        #arrivals bttn
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 420, 111, 23))
        self.pushButton_2.setText("Project Arrivals")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.arrivals_project_bttn)

        
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(50, 490, 111, 23))
        self.pushButton_3.setText("Back Menu")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.go_to_main_menu)
        

        # Table
        self.tableWidget = QtWidgets.QTableWidget(parent=self.frame)
        self.tableWidget.setGeometry(QtCore.QRect(240, 220, 471, 221))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)



        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Pencere açılır açılmaz veri çek
        self.send_request()
        

    def submitted_project_bttn(self):
        match_rows = [data for data in self.alldata if bool(data.get("Proje gonderilis tarihi"))]
        self.update_table_widget(match_rows)

    def arrivals_project_bttn(self):
        match_rows = [data for data in self.alldata if bool(data.get("Projenin gelis tarihi"))]
        self.update_table_widget(match_rows)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Interviews"))
        self.interviews.setText(_translate("MainWindow", "INTERVIEWS"))
        self.menu.setText(_translate("MainWindow", "MENU"))

    def search_button(self):
        search_text = self.linesearch.text().strip().lower()
        match_rows = []

        for row_data in self.alldata:  # alldata üzerinden filtre
                if any(search_text in str(value).lower() for value in row_data.values()):
                        match_rows.append(row_data)

        self.update_table_widget(match_rows)


    def update_table_widget(self, match_rows):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(match_rows))

        if not match_rows:
                return

        headers = list(match_rows[0].keys())
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for row, row_data in enumerate(match_rows):
                for col, value in enumerate(row_data.values()):  # <-- value’ları kullan
                        self.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))

    def send_request(self):
        url = "http://127.0.0.1:8002/interviews"
        try:
            resp = requests.get(url, timeout=8)
            data = resp.json()

            if resp.status_code == 200 and data:
                # Dinamik kolonlar
                headers = list(data[0].keys())
                self.tableWidget.setColumnCount(len(headers))
                self.tableWidget.setHorizontalHeaderLabels(headers)

                self.alldata = data
                self.tableWidget.setRowCount(len(data))
                for row, item in enumerate(data):
                    for col, key in enumerate(headers):
                        self.tableWidget.setItem(row, col, QTableWidgetItem(str(item.get(key, ""))))
            else:
                QtWidgets.QMessageBox.information(None, "Error", "Error fetching data")
        except Exception as e:
            QtWidgets.QMessageBox.information(None, "Error", str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Interviews()
    window.show()
    sys.exit(app.exec())

