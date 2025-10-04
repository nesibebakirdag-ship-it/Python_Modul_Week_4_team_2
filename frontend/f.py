import sys
import os
from PyQt6 import QtWidgets, uic
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
from dotenv import load_dotenv
import os

load_dotenv() 



class CreateUserWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(r".\ui\second.ui", self)

        # 🔸 Butona tıklayınca yeni kullanıcı ekleme işlemi başlatılacak
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
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text().strip()
        role = self.roleComboBox.currentText().strip()

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
                range=f"{os.getenv("SHEET_NAME")}!A:D",      # A: username, B: password, C: role, D: tarih
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body=body
            ).execute()

            QtWidgets.QMessageBox.information(self, "Başarılı", f"{username} adlı kullanıcı eklendi.")

            # Formu temizle
            self.usernameInput.clear()
            self.passwordInput.clear()
            self.roleComboBox.setCurrentIndex(0)

        except HttpError as error:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Google Sheets API hatası:\n{error}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = CreateUserWindow()
    w.show()
    sys.exit(app.exec())
