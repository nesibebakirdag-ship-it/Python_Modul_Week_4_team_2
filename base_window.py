from PyQt6 import QtWidgets, uic

class BaseWindow(QtWidgets.QMainWindow):
    """
    Base class for all windows. Provides common navigation utilities.
    """
    def open_menu(self, window_class):
        """Open another window inheriting BaseWindow."""
        self.next_window = window_class()
        self.next_window.show()
        self.hide()

    def go_to_main_menu(self):
        from preference import PreferenceWindow
        self.open_menu(PreferenceWindow)

    def go_to_preferences(self):
        from preference import PreferenceWindow
        self.open_menu(PreferenceWindow)

    def confirm_exit(self):
            reply = QtWidgets.QMessageBox.question(
             self,
                "Exit Confirmation",
                     "Are you sure you want to exit?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
             )

            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                QtWidgets.QApplication.quit()
