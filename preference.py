from PyQt6 import QtCore, QtGui, QtWidgets, uic
from admin import Admin
from applicaton import Applications
from mentor import Mentor
from Interviews import Interviews


class PreferenceWindow(QtWidgets.QMainWindow):
    def __init__(self, role):
        super().__init__()
        # UI dosyasını yükle
        uic.loadUi("ui/preferenceadmin.ui", self)
        
        # Role bazlı admin buton görünürlüğü
        if role == "admin":
            self.admin_menu.show()
        else:
            self.admin_menu.hide()
        
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
        QtWidgets.QApplication.instance().quit()

    def btn_main(self):
        # Örnek: main menü açmak istiyorsan burayı düzenle
        QtWidgets.QMessageBox.information(self, "Info", "Main menu clicked!")

    def btn_admin(self):
        self.open_menu(Admin)

    # Genel menü açma metodu
    def open_menu(self, page_class):
        self.menu_window = page_class()
        self.menu_window.show()
        self.close()


# Test için çalıştırılabilir
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # role="admin" veya "user" deneyebilirsin
    window = PreferenceWindow(role="admin")
    window.show()
    sys.exit(app.exec())
