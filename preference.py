from PyQt6 import QtCore, QtGui, QtWidgets, uic
from applicaton import Applications
from mentor import Mentor
from Interviews import Interviews
from session import Session
from base_window import BaseWindow
from etkinlik import CalendarApp
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal


class PreferenceWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        # UI dosyasını yükle
        uic.loadUi("ui/preferenceadmin.ui", self)
        
        session = Session()

        # Role bazlı admin buton görünürlüğü
        if session.role == "admin":
            self.admin_menu.show()
            self.label_2 = "CRM - Preference Admin Menu"
        else:
            self.admin_menu.hide()
            self.label_2 = "CRM - Preference Menu"
        
      

        # Butonların click olaylarını bağla
        self.applications.clicked.connect(self.btn_application)
        self.interviews.clicked.connect(self.btn_interviews)
        self.mentor_meet.clicked.connect(self.btn_mentor)
        self.exit.clicked.connect(self.btn_exit)
        self.main_menu.clicked.connect(self.btn_main)
        self.admin_menu.clicked.connect(self.btn_admin)

    # Buton metodları
    def btn_application(self):
        self.open_menu(Applications)

    def btn_interviews(self):
        self.open_menu(Interviews)

    def btn_mentor(self):
        self.open_menu(Mentor)

    def btn_exit(self):
        self.confirm_exit()

    def btn_main(self):
       self.open_menu(PreferenceWindow)

    def btn_admin(self):
        self.open_menu(CalendarApp)


# Test için çalıştırılabilir
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # role="admin" veya "user" deneyebilirsin
    window = PreferenceWindow(role="admin")
    window.show()
    sys.exit(app.exec())
