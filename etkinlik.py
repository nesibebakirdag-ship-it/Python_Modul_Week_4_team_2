import sys
import os
import datetime
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import subprocess
from mail import MainWindow
from dotenv import load_dotenv
import os

load_dotenv() 

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/spreadsheets"
]






# 🟨 İkinci pencereyi temsil eden sınıf
class UserWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r".\ui\second.ui", self)  # ← Burada açılacak UI dosyasını belirtiyorsun

        self.pushButton.clicked.connect(self.create_user)

    def get_credentials(self):
        """Google Sheets API kimlik doğrulama"""
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "eskicredentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def create_user(self):
        """Formdaki verileri alır ve Google Sheet'e yeni kullanıcı olarak ekler"""
        username = self.username.text().strip()
        password = self.password.text().strip()
        role = self.role.currentText().strip()

        # Basit doğrulama
        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Eksik Bilgi", "Lütfen kullanıcı adı ve şifre girin.")
            return

        creds = self.get_credentials()

        try:
            service = build("sheets", "v4", credentials=creds)

            # 📌 Sheets'e eklenecek satır verisi
            values = [[
                username,
                password,
                role,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ]]

            body = {"values": values}

            result = service.spreadsheets().values().append(
                spreadsheetId=os.getenv("SPREADSHEET_ID"),
                range=os.getenv("SHEET_NAME"),      # A: username, B: password, C: role, D: tarih
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body=body
            ).execute()

            QtWidgets.QMessageBox.information(self, "Başarılı", f"{username} adlı kullanıcı eklendi.")

            # Formu temizle
            self.username.clear()
            self.password.clear()
            self.role.setCurrentIndex(0)

        except HttpError as error:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Google Sheets API hatası:\n{error}")
        
# class MailWindow(QtWidgets.QMainWindow, MainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)   

class UserWindow2(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r".\ui\mail.ui", self)
        
    

# 🟦 Ana pencere (Calendar)
class CalendarApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r".\ui\u.ui", self)

        # Etkinlikleri yükleyen buton
        self.pushButton.clicked.connect(self.load_events)

        # 🔸 Bu buton başka bir UI açacak (Qt Designer'daki objectName = openUserPageButton)
        self.createUserButton.clicked.connect(self.open_user_window)
        self.mailbutton.clicked.connect(self.open_user_window2)

    def open_user_window2(self):
        """Diğer UI dosyasını açar"""
        self.user_window = UserWindow2()
        self.user_window.show()

    def open_user_window(self):
        """Diğer UI dosyasını açar"""
        self.user_window = UserWindow()
        self.user_window.show()
        

    def load_events(self):
        """Google Calendar etkinliklerini çekip tabloya tüm bilgileriyle yazar."""
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            service = build("calendar", "v3", credentials=creds)
            now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=50,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)

            if not events:
                self.tableWidget.setColumnCount(1)
                self.tableWidget.setHorizontalHeaderLabels(["Bilgi"])
                self.tableWidget.insertRow(0)
                self.tableWidget.setItem(0, 0, QTableWidgetItem("Hiç etkinlik bulunamadı."))
                return

            headers = [
                "ID",
                "Başlık",
                "Açıklama",
                "Konum",
                "Başlangıç",
                "Bitiş",
                "Oluşturan",
                "Katılımcılar",
                "Durum",
                "HTML Link"
            ]
            self.tableWidget.setColumnCount(len(headers))
            self.tableWidget.setHorizontalHeaderLabels(headers)

            for i, event in enumerate(events):
                event_id = event.get("id", "")
                summary = event.get("summary", "")
                description = event.get("description", "")
                location = event.get("location", "")
                start = event.get("start", {}).get("dateTime", event.get("start", {}).get("date", ""))
                end = event.get("end", {}).get("dateTime", event.get("end", {}).get("date", ""))
                creator = event.get("creator", {}).get("email", "")
                attendees = ", ".join([a.get("email", "") for a in event.get("attendees", [])]) if "attendees" in event else ""
                status = event.get("status", "")
                html_link = event.get("htmlLink", "")

                values = [
                    event_id,
                    summary,
                    description,
                    location,
                    start,
                    end,
                    creator,
                    attendees,
                    status,
                    html_link
                ]

                self.tableWidget.insertRow(i)
                for col, val in enumerate(values):
                    item = QTableWidgetItem(str(val))
                    self.tableWidget.setItem(i, col, item)

            self.tableWidget.resizeColumnsToContents()

        except HttpError as error:
            print(f"Bir hata oluştu: {error}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec())
