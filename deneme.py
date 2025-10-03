import sys
import os
import datetime
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem, QInputDialog, QComboBox, QDialog, QVBoxLayout, QLabel, QPushButton

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os

load_dotenv() 



# ✅ Hem Calendar hem Sheets erişimi için gerekli izinler
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/spreadsheets"
]



class RoleDialog(QDialog):
    """Email ve rol seçimi için basit bir input dialog"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yeni Kullanıcı Ekle")

        layout = QVBoxLayout()

        self.email_label = QLabel("Email adresi:")
        layout.addWidget(self.email_label)

        self.email_input = QtWidgets.QLineEdit()
        layout.addWidget(self.email_input)

        self.role_label = QLabel("Rol seçin:")
        layout.addWidget(self.role_label)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["admin", "user"])
        layout.addWidget(self.role_combo)

        self.ok_button = QPushButton("Ekle")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_data(self):
        return self.email_input.text().strip(), self.role_combo.currentText()


class CalendarApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r".\ui\admin.ui", self)

        # Etkinlikleri yükleme butonu
        self.pushButton.clicked.connect(self.load_events)

        # ✅ Create User butonu (Qt Designer'daki objectName bu olmalı)
        

    def get_credentials(self):
        """Google API kimlik doğrulaması"""
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
        return creds

    def load_events(self):
        """Google Calendar etkinliklerini tabloya yükler"""
        creds = self.get_credentials()

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
                "ID", "Başlık", "Açıklama", "Konum",
                "Başlangıç", "Bitiş", "Oluşturan",
                "Katılımcılar", "Durum", "HTML Link"
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

                values = [event_id, summary, description, location, start, end, creator, attendees, status, html_link]

                self.tableWidget.insertRow(i)
                for col, val in enumerate(values):
                    self.tableWidget.setItem(i, col, QTableWidgetItem(str(val)))

            self.tableWidget.resizeColumnsToContents()

        except HttpError as error:
            print(f"Bir hata oluştu: {error}")

    def create_user(self):
        """Yeni kullanıcıyı Google Sheets'e ekler"""
        dialog = RoleDialog()
        if dialog.exec():
            email, role = dialog.get_data()

            if not email:
                QtWidgets.QMessageBox.warning(self, "Hata", "Email adresi boş olamaz.")
                return

            creds = self.get_credentials()

            try:
                service = build("sheets", "v4", credentials=creds)

                # Google Sheet'e eklenecek veri
                values = [[email, role, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]]
                body = {"values": values}

                result = service.spreadsheets().values().append(
                    spreadsheetId=os.getenv("SPREADSHEET_ID"),
                    range=f"{os.getenv("SHEET_NAME")}!A:C",
                    valueInputOption="USER_ENTERED",
                    insertDataOption="INSERT_ROWS",
                    body=body
                ).execute()

                QtWidgets.QMessageBox.information(self, "Başarılı", f"{email} ({role}) eklendi.")

            except HttpError as error:
                QtWidgets.QMessageBox.critical(self, "Google Sheets Hatası", str(error))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec())
