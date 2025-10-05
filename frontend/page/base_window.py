import sys
import os
from PyQt6 import QtWidgets, uic, QtGui

# -------------------------------
# Central project paths
# -------------------------------
# frontend dizinini baz al
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # frontend/
UI_PATH = os.path.join(PROJECT_ROOT, "ui")
IMG_PATH = os.path.join(PROJECT_ROOT, "img")

# -------------------------------
# BaseWindow: all windows inherit this
# -------------------------------
class BaseWindow(QtWidgets.QMainWindow):
    _session = None  # centralized session

    def __init__(self):
        super().__init__()

        # -------------------------------
        # Load UI file if given
        # -------------------------------
            
            
    def get_ui(self,ui_file):
        if ui_file:
            full_ui_path = os.path.join(UI_PATH, ui_file)
            if not os.path.exists(full_ui_path):
                raise FileNotFoundError(f"UI file not found: {full_ui_path}")
        return full_ui_path
    # -------------------------------
    # Helper: load logo/image into a QLabel
    # -------------------------------
    def set_logo(self,  filename: str):
        img_file = os.path.join(IMG_PATH, filename)
        if not os.path.exists(img_file):
            raise FileNotFoundError(f"Image not found: {img_file}")
        return QtGui.QPixmap(img_file)


    # -------------------------------
    # Centralized session getter
    # -------------------------------
    @classmethod
    def get_session(cls):
        if cls._session is None:
            from .utils.session import session
            cls._session = session
        return cls._session

    # -------------------------------
    # Open another window and hide current
    # -------------------------------
    def open_menu(self, page_class):
        new_window = page_class()
        new_window.show()
        self.hide()

    # -------------------------------
    # Quick navigation helpers
    # -------------------------------
    def go_to_main_menu(self):
        from .preference import PreferenceWindow
        self.open_menu(PreferenceWindow)

    def go_to_preferences(self):
        from .preference import PreferenceWindow
        self.open_menu(PreferenceWindow)

    # -------------------------------
    # Exit confirmation
    # -------------------------------
    def confirm_exit(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Exit Confirmation",
            "Are you sure you want to exit?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            QtWidgets.QApplication.quit()
