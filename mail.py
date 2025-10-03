import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox
from PyQt6 import uic
import sys

Ui_MainWindow, QtBaseClass = uic.loadUiType(r'.\ui\mail.ui')

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Artık combobox direkt self.candidatesComboBox ile erişilebilir
        self.calendar_manager = GoogleCalendarManager()
        self.load_emails_to_combobox()
        print("Google Calendar'dan email adresleri yüklendi.")
    def load_emails_to_combobox(self):
        try:
            self.candidatesComboBox.clear()
            emails = self.calendar_manager.get_emails_from_events()
            if emails:
                self.candidatesComboBox.addItems(emails)
            else:
                self.candidatesComboBox.addItem("Email bulunamadı")
        except Exception as e:
            print(f"Hata: {e}")
            self.candidatesComboBox.addItem("Yükleme hatası")


class GoogleCalendarManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('calendar', 'v3', credentials=creds)
    
    def get_emails_from_events(self, max_results=50):
        try:
            emails = set()
            events_result = self.service.events().list(
                calendarId='primary',
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            for event in events:
                attendees = event.get('attendees', [])
                for attendee in attendees:
                    email = attendee.get('email')
                    if email and '@' in email:
                        emails.add(email)
                
                organizer = event.get('organizer', {})
                organizer_email = organizer.get('email')
                if organizer_email and '@' in organizer_email:
                    emails.add(organizer_email)
            
            return sorted(list(emails))
        except Exception as e:
            print(f"Google Calendar'dan veri çekilirken hata: {e}")
            return []

# ---- Program başlatma ----
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
