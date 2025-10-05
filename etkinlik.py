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
from dotenv import load_dotenv
import os
import base64
from email.mime.text import MIMEText
from base_window import BaseWindow

load_dotenv() 

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
     "https://www.googleapis.com/auth/gmail.send"
]






# 🟨 İkinci pencereyi temsil eden sınıf
class CreateUser(QtWidgets.QMainWindow):
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
                    "API/config/vit8-credentials.json", SCOPES
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
class Mail(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r".\ui\mail.ui", self)

        self.event_dict = {}  # { "Etkinlik Başlığı": ["mail1", "mail2"] }
        self.load_calendar_events()

        self.comboBox.currentIndexChanged.connect(self.update_email_field)
        self.pushButton.clicked.connect(self.send_email_to_selected)

    def load_calendar_events(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
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

            self.comboBox.clear()
            self.event_dict.clear()

            if not events:
                self.comboBox.addItem("Hiç etkinlik bulunamadı.")
                return

            for event in events:
                title = event.get("summary", "(Başlıksız Etkinlik)")
                attendees = event.get("attendees", [])
                email_list = [att.get("email", "").strip() for att in attendees if att.get("email")]
                self.event_dict[title] = email_list

            self.comboBox.addItems(sorted(self.event_dict.keys()))

        except HttpError as error:
            self.comboBox.clear()
            self.comboBox.addItem(f"Hata: {error}")

    def update_email_field(self):
        selected_event = self.comboBox.currentText()
        if selected_event in self.event_dict:
            emails = self.event_dict[selected_event]
            self.textEdit.setPlainText("\n".join(emails))
        else:
            self.textEdit.clear()

    def send_email_to_selected(self):
        """textEdit içindeki mail adreslerine mail gönderir."""
        subject = self.textEdit_2.toPlainText().strip()
        body = self.textEdit_3.toPlainText().strip()

        raw_emails = self.textEdit.toPlainText().strip()
        recipients = [e.strip() for e in raw_emails.splitlines() if e.strip()]

        if not recipients:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen textEdit içine en az bir e-posta adresi girin.")
            return

        if not subject or not body:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen konu ve mesaj içeriğini doldurun.")
            return

        try:
            creds = None
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                    creds = flow.run_local_server(port=0)
                with open("token.json", "w") as token:
                    token.write(creds.to_json())

            service = build('gmail', 'v1', credentials=creds)

            for to_email in recipients:
                message = MIMEText(body)
                message['to'] = to_email
                message['subject'] = subject

                raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
                send_message = {'raw': raw_message}

                service.users().messages().send(userId="me", body=send_message).execute()

            QtWidgets.QMessageBox.information(self, "Başarılı", f"{len(recipients)} kişiye mail gönderildi ✅")

        except HttpError as error:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Mail gönderirken hata oluştu:\n{error}")


    

# 🟦 Ana pencere (Calendar)
class CalendarApp(BaseWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r".\ui\u.ui", self)

        # Etkinlikleri yükleyen buton
        self.pushButton.clicked.connect(self.load_events)

        # 🔸 Bu buton başka bir UI açacak (Qt Designer'daki objectName = openUserPageButton)
        self.createUserButton.clicked.connect(self.open_user_window)
        self.mailbutton.clicked.connect(self.open_user_window2)
        self.pushButton_3.clicked.connect(self.confirm_exit)
        self.pushButton_5.clicked.connect(self.go_to_main_menu)
        #5 main
        #3 exit

    def open_user_window2(self):
        """Diğer UI dosyasını açar"""
        self.user_window = Mail()
        self.user_window.show()

    def open_user_window(self):
        """Diğer UI dosyasını açar"""
        self.user_window = CreateUser()
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
                    "API/config/vit8-credentials.json", SCOPES)
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
