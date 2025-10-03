import sys
import pandas as pd
from PyQt6 import QtWidgets, uic
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv() 



# 🧠 Google Sheets API Servisini oluştur
def get_service():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file(os.getenv("CREDENTIALS_FILE"), scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)
    return service

# 📥 Google Sheets'ten veriyi DataFrame olarak çek
def read_google_sheet():
    service = get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=os.getenv("SPREADSHEET_ID"),
        range=os.getenv("FSHEET_NAME")
    ).execute()

    values = result.get('values', [])
    if not values:
        return pd.DataFrame()
    else:
        return pd.DataFrame(values[1:], columns=values[0])  # ilk satır başlık

# 🧭 PyQt6 Arayüzü
class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r".\ui\admin.ui", self)  # senin UI dosyanın adı

        # 📌 tableWidget ismi senin UI'daki tabloyla aynı olmalı!
        self.load_table_data()

    def load_table_data(self):
        df = read_google_sheet()
        if df.empty:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Google Sheet'ten veri alınamadı.")
            return

        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setHorizontalHeaderLabels(df.columns)

        for row in range(len(df)):
            for col in range(len(df.columns)):
                item = QtWidgets.QTableWidgetItem(str(df.iat[row, col]))
                self.tableWidget.setItem(row, col, item)

        self.tableWidget.resizeColumnsToContents()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())



# class MyWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(MyWindow, self).__init__()
#         uic.loadUi(r".\ui\admin.ui", self)  # .ui dosyasını yükler
#         self.pushButton.clicked.connect(self.butonTiklandi)

#     def butonTiklandi(self):
#         print("Butona tıklandı!")

# app = QtWidgets.QApplication(sys.argv)
# window = MyWindow()
# window.show()
# sys.exit(app.exec())  # PyQt6 tarzı
