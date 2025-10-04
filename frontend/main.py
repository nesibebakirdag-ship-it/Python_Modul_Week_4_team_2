# main.py
import sys
import os
from PyQt6 import QtWidgets

# 1️⃣ Proje dizinini Python path'e ekle
# Bu, tüm frontend klasörünü ve alt klasörlerini import edilebilir yapar
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
FRONTEND_PATH = os.path.join(PROJECT_ROOT, "frontend")
if FRONTEND_PATH not in sys.path:
    sys.path.insert(0, FRONTEND_PATH)

# 2️⃣ Artık page ve enum alt klasörlerinden import edebilirsin
from page.Login import Ui_MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec())
